"""Physics, fault and ADC models (ground truth fidelity, goal G2)."""

from datetime import datetime

import numpy as np
import pytest

from sim import adc
from sim.config import Fault, Scenario
from sim.firmware_model import read_current, read_voltage
from sim.physics import Environment


@pytest.mark.covers("HARN-SCEN")
def test_clear_sky_day_shape():
    sc = Scenario.load("clear_day").model_copy(
        update={"start": datetime(2020, 5, 15), "duration_s": 86400}
    )
    env = Environment(sc)
    g = [env.irradiance(h * 3600) for h in np.arange(0, 24, 0.25)]  # 00:00..23:45 IST
    assert max(g[: 4 * 5]) == 0 and max(g[4 * 20 :]) == 0  # dark before 05:00 and after 20:00
    assert g[4 * 18] > 50  # mid-May sunset at 78.5 E is ~18:45 IST
    peak_h = 0.25 * int(np.argmax(g))
    assert 11.5 <= peak_h <= 13.0  # solar noon ~12:15 IST at 78.5 E
    assert 900 < max(g) < 1150


@pytest.mark.covers("HARN-SCEN")
def test_night_is_dark():
    env = Environment(Scenario.load("night"))
    tr = env.rig_truth(1800)
    assert tr["irradiance_wm2"] == 0 and tr["V_A"] == 0 and tr["I_D"] == 0


@pytest.mark.covers("HARN-SCEN")
def test_clouds_seeded_and_bounded():
    a = Environment(Scenario.load("cloudy_day")).kt
    b = Environment(Scenario.load("cloudy_day")).kt
    c = Environment(Scenario.load("cloudy_day").model_copy(update={"seed": 7})).kt
    assert np.array_equal(a, b) and not np.array_equal(a, c)
    assert a.min() >= 0.2 and a.max() <= 1.0 and a.std() > 0.05


@pytest.mark.covers("HARN-SCEN")
def test_fault_windows():
    sc = Scenario.load("lab_bench")
    sc.faults = [
        Fault(kind="disconnect", target="B", start_s=10, end_s=20),
        Fault(kind="shading", target="C", value=0.9),
        Fault(kind="degradation", target="A", value=0.5),
    ]
    env = Environment(sc)
    assert (
        env.rig_truth(5)["V_B"] > 5
        and env.rig_truth(15)["V_B"] == 0
        and env.rig_truth(25)["V_B"] > 5
    )
    nominal = env.panel("D", 0).voltage
    assert env.rig_truth(0)["V_C"] < nominal
    assert env.rig_truth(0)["V_A"] == pytest.approx(nominal * 0.5)


@pytest.mark.covers("FEAT-CAL")
def test_ideal_adc_round_trip_within_quantisation():
    # analogReadMilliVolts() has 1 mV steps: 3.03 mV per panel volt, 8.1 mA per amp
    for v in np.linspace(0, 9.99, 400):
        mv = round(adc.pin_mv(adc.voltage_pin(v), "ideal"))
        assert abs(read_voltage(mv) - v) <= 0.5e-3 * 10 / 3.3 + 1e-6
    for i in np.linspace(0, 4.5, 200):
        mv = round(adc.pin_mv(adc.current_pin(i), "ideal"))
        assert abs(read_current(mv) - i) <= 0.5e-3 / adc.ACS_DIVIDER_RATIO / 0.185 + 1e-6


@pytest.mark.covers("FEAT-CAL")
def test_sensor_faults_on_raw_codes():
    sc = Scenario.load("sensor_faults")
    env = Environment(sc)
    raws = lambda t: adc.to_raw(sc, env.rig_truth(t), int(t * 1000))
    assert raws(700)[adc.PIN_C] == 1200  # stuck
    assert raws(1300)[adc.PIN_D] == 4095  # saturated
    assert raws(1900)[adc.PIN_D] < 4095
    noisy = {raws(t)[adc.PIN_A] for t in range(0, 40, 2)}
    assert len(noisy) > 5  # noise varies the reading
    assert raws(30) == raws(30)  # but deterministically


@pytest.mark.covers("FEAT-CAL")
def test_readings_accurate_on_physical_esp32_adc():
    """F4: calibrated mV + explicit dividers stay accurate on the non-linear ESP32 ADC."""
    sc = Scenario.load("esp32_adc_physical")
    for i in np.linspace(0.0, 4.5, 46):
        truth = {"V_A": 6.0, "V_B": 6.0, "V_C": 6.0, "I_D": float(i)}
        s = adc.sample(sc, truth, 0)
        assert read_current(s.mv[adc.PIN_D]) == pytest.approx(i, abs=0.01)
    for v in np.linspace(0.5, 9.0, 35):
        truth = {"V_A": float(v), "V_B": 0.0, "V_C": 0.0, "I_D": 0.0}
        s = adc.sample(sc, truth, 0)
        assert read_voltage(s.mv[adc.PIN_A]) == pytest.approx(v, abs=0.005)


@pytest.mark.covers("FEAT-CAL")
def test_raw_adc_codes_would_be_inaccurate():
    """Why F4 switched away from raw analogRead(): the old formula on raw ESP32 codes."""
    raw = round(adc.esp32_current_raw(1.0))
    old_formula = ((raw / 4095.0) * 5.0 - 2.5) / 0.185
    assert abs(old_formula - 1.0) > 0.5


@pytest.mark.covers("FEAT-CAL")
def test_unsupported_wiring_without_acs_divider_saturates():
    """Without the 2:3 divider GPIO33 is over-driven: readings pin near the 3.1 V ceiling."""
    sc = Scenario.load("esp32_adc_physical").model_copy(update={"acs_divider": False})
    s = adc.sample(sc, {"V_A": 6.0, "V_B": 6.0, "V_C": 6.0, "I_D": 4.0}, 0)
    assert s.mv[adc.PIN_D] == round(adc.ESP32_SAT_V * 1000)
