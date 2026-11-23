"""Virtual ADC bus: physical quantities -> what the ESP32 reads on GPIO 34/35/32/33.

Every sample carries two readings per pin:
  * ``raw`` - the 12-bit ``analogRead()`` code, and
  * ``mv``  - the eFuse-calibrated ``analogReadMilliVolts()`` value the firmware uses (F4).

Signal chain (rig wiring, see README):
  * Panel voltage -> resistive divider 10 V : 3.3 V -> GPIO 34/35/32.
  * ACS712-05B output (2.5 V + 0.185 V/A) -> 2:3 divider (10 kΩ/20 kΩ) -> GPIO 33.
    ``acs_divider: false`` models the unsupported direct connection (pin over-driven).

Two ADC models:
  * ``ideal``  - perfectly linear 0-3.3 V converter (raw = v/3.3*4095, mv = v*1000).
  * ``esp32``  - physically faithful raw codes (dead zone below ~0.1 V, mid-scale bow,
                 saturation near 3.1 V at 11 dB). Calibrated mV removes the non-linearity
                 but still saturates near 3.1 V.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import Scenario

PIN_A, PIN_B, PIN_C, PIN_D = 34, 35, 32, 33
PIN_OF = {"A": PIN_A, "B": PIN_B, "C": PIN_C, "D": PIN_D}
ADC_MAX = 4095

ACS_OFFSET_V = 2.5
ACS_SENS_V_PER_A = 0.185
ACS_DIVIDER_RATIO = 2.0 / 3.0  # GPIO33 volts per ACS712 output volt (10k series / 20k to GND)
V_FULL_SCALE = 10.0  # panel volts that map to the 3.3 V pin full scale
VREF = 3.3
PIN_PER_PANEL_V = VREF / V_FULL_SCALE
ESP32_KNEE_LO = 0.10  # below this the raw ESP32 ADC reads 0
ESP32_SAT_V = 3.10  # ~where readings pin at full scale (11 dB attenuation)


@dataclass
class AdcSample:
    raw: dict[int, int]
    mv: dict[int, int]


def voltage_pin(v_panel: float) -> float:
    return max(v_panel, 0.0) * PIN_PER_PANEL_V


def current_pin(i: float, divider: bool = True) -> float:
    return (ACS_OFFSET_V + ACS_SENS_V_PER_A * max(i, -5.0)) * (
        ACS_DIVIDER_RATIO if divider else 1.0
    )


def ideal_pin_raw(v_pin: float) -> float:
    return v_pin / VREF * ADC_MAX


def esp32_pin_raw(v_pin: float) -> float:
    """Approximate ESP32 ADC transfer (11 dB): dead zone, mild bow, hard saturation."""
    if v_pin <= ESP32_KNEE_LO:
        return 0.0
    x = (min(v_pin, ESP32_SAT_V) - ESP32_KNEE_LO) / (ESP32_SAT_V - ESP32_KNEE_LO)
    return ADC_MAX * (x + 0.03 * x * (1 - x))  # ~+0.75% bow mid-scale


def pin_mv(v_pin: float, model: str) -> float:
    """analogReadMilliVolts(): calibrated (linear) but limited by the input range."""
    top = VREF if model == "ideal" else ESP32_SAT_V
    return min(max(v_pin, 0.0), top) * 1000.0


def mv_from_raw(raw: int) -> int:
    """Linear mV equivalent of a raw code (used when a caller only provides raw codes)."""
    return round(raw * VREF * 1000 / ADC_MAX)


def ideal_voltage_raw(v: float) -> float:
    return ideal_pin_raw(voltage_pin(v))


def ideal_current_raw(i: float) -> float:
    return ideal_pin_raw(current_pin(i))


def esp32_voltage_raw(v: float) -> float:
    return esp32_pin_raw(voltage_pin(v))


def esp32_current_raw(i: float, divider: bool = True) -> float:
    return esp32_pin_raw(current_pin(i, divider))


def _rng(sc: Scenario, t_ms: int, pin: int) -> np.random.Generator:
    return np.random.default_rng([sc.seed, int(t_ms), pin])


def sample(sc: Scenario, truth: dict, t_ms: int) -> AdcSample:
    """Map physical truth to ADC readings, applying sensor/ADC faults and noise."""
    t_s = t_ms / 1000.0
    values = {"A": truth["V_A"], "B": truth["V_B"], "C": truth["V_C"], "D": truth["I_D"]}
    raw_out: dict[int, int] = {}
    mv_out: dict[int, int] = {}
    for name, val in values.items():
        pin = PIN_OF[name]
        rng = _rng(sc, t_ms, pin)
        stuck = saturated = None
        for f in sc.faults:
            if not (f.active(t_s) and f.hits(name)):
                continue
            if f.kind == "sensor_noise" and f.value > 0:
                val = val + rng.normal(0.0, f.value)
            elif f.kind == "sensor_stuck":
                stuck = int(f.value)
            elif f.kind == "adc_saturation":
                saturated = True
        v_pin = current_pin(val, sc.acs_divider) if name == "D" else voltage_pin(val)
        raw = ideal_pin_raw(v_pin) if sc.adc_model == "ideal" else esp32_pin_raw(v_pin)
        mv = pin_mv(v_pin, sc.adc_model)
        if sc.adc_noise_lsb > 0:
            n = rng.normal(0.0, sc.adc_noise_lsb)
            raw += n
            mv += n * VREF * 1000 / ADC_MAX
        code = int(np.clip(round(raw), 0, ADC_MAX))
        mvi = int(np.clip(round(mv), 0, round(VREF * 1000)))
        if saturated:
            code, mvi = ADC_MAX, round((VREF if sc.adc_model == "ideal" else ESP32_SAT_V) * 1000)
        if stuck is not None:
            code = int(np.clip(stuck, 0, ADC_MAX))
            mvi = mv_from_raw(code)
        raw_out[pin], mv_out[pin] = code, mvi
    return AdcSample(raw_out, mv_out)


def to_raw(sc: Scenario, truth: dict, t_ms: int) -> dict[int, int]:
    return sample(sc, truth, t_ms).raw
