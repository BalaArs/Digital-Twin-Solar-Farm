"""Bit-faithful Python port of Solar_Farm.ino (reference model).

Mirrors the firmware's float32 arithmetic and string formatting so its output can be
byte-compared against the real sketch running in the firmware-in-the-loop (FIL) harness.
Keep this file in sync with Solar_Farm.ino: tests/test_fil.py fails when they diverge.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .adc import PIN_A, PIN_B, PIN_C, PIN_D, mv_from_raw

RED_AB, YELLOW_AB, GREEN_AB = 14, 12, 13
RED_CD, YELLOW_CD, GREEN_CD = 25, 26, 27
LED_PINS = (RED_AB, YELLOW_AB, GREEN_AB, RED_CD, YELLOW_CD, GREEN_CD)

STATUS_RED = "RED: No Voltage"
STATUS_YELLOW = "YELLOW: Low Voltage"
STATUS_GREEN = "GREEN: Normal"

f32 = np.float32


VOLTAGE_DIVIDER_GAIN = 10.0 / 3.3  # #define VOLTAGE_DIVIDER_GAIN (10.0 / 3.3)
ACS_DIVIDER_RATIO = 2.0 / 3.0  # #define ACS_DIVIDER_RATIO (2.0 / 3.0)
ACS_ZERO_MV = 2500.0
ACS_MV_PER_A = 185.0


def read_voltage(mv: int) -> float:
    # uint32_t mv = analogReadMilliVolts(pin); float voltage = (mv / 1000.0) * VOLTAGE_DIVIDER_GAIN;
    return float(f32((mv / 1000.0) * VOLTAGE_DIVIDER_GAIN))


def read_current(mv: int) -> float:
    # float sensorMv = mv / ACS_DIVIDER_RATIO; float current = (sensorMv - ACS_ZERO_MV) / ACS_MV_PER_A;
    s = float(f32(mv / ACS_DIVIDER_RATIO))
    c = float(f32((s - ACS_ZERO_MV) / ACS_MV_PER_A))
    return 0.0 if c < 0 else c


def readings(raws: dict[int, int], mvs: dict[int, int] | None) -> tuple[float, float, float, float]:
    """The four firmware readings from calibrated mV (derived from raw codes if absent)."""
    mv = mvs if mvs is not None else {p: mv_from_raw(r) for p, r in raws.items()}
    return (
        read_voltage(mv[PIN_A]),
        read_voltage(mv[PIN_B]),
        read_voltage(mv[PIN_C]),
        read_current(mv[PIN_D]),
    )


def classify(v: float) -> str:
    if v <= 1.0:
        return STATUS_RED
    if v < 5.0:
        return STATUS_YELLOW
    return STATUS_GREEN


def led_levels(status: str, red: int, yellow: int, green: int) -> dict[int, int]:
    return {
        red: int(status == STATUS_RED),
        yellow: int(status == STATUS_YELLOW),
        green: int(status == STATUS_GREEN),
    }


def fmt2(x: float) -> str:
    """Arduino String(float, 2) / printf("%.2f") of a float promoted to double."""
    return f"{x:.2f}"


@dataclass
class HttpResponse:
    status: int
    content_type: str
    body: str
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class Events:
    blynk: list[tuple[int, object]] = field(default_factory=list)  # (virtual pin, value)
    leds: dict[int, int] = field(default_factory=dict)  # final level per GPIO
    serial: list[str] = field(default_factory=list)


class FirmwareModel:
    """Stateful model: statusAB/statusC persist between sendData() and handleAPI()."""

    name = "python"

    def __init__(self) -> None:
        self.status_ab = ""
        self.status_c = ""

    def setup(self) -> Events:
        ev = Events()  # setup() only calls pinMode(): no LED writes
        ev.serial = ["Connecting WiFi", "Wi-Fi Connected! IP: ", "127.0.0.1", "API Ready"]
        return ev

    def update_leds(self, va: float, vb: float, vc: float) -> dict[int, int]:
        self.status_ab = classify(min(va, vb))  # groupAB(): weakest panel
        self.status_c = classify(vc)
        leds = led_levels(self.status_ab, RED_AB, YELLOW_AB, GREEN_AB)
        leds.update(led_levels(self.status_c, RED_CD, YELLOW_CD, GREEN_CD))
        return leds

    def tick(self, t_ms: int, raws: dict[int, int], mvs: dict[int, int] | None = None) -> Events:
        """sendData(): fired by BlynkTimer every 2000 ms."""
        va, vb, vc, cd = readings(raws, mvs)
        ev = Events()
        ev.blynk = [(0, va), (1, vb), (2, vc), (3, cd)]
        ev.leds = self.update_leds(va, vb, vc)
        ev.blynk += [(4, self.status_ab), (5, self.status_c)]
        ev.serial = [
            f"A: {fmt2(va)} V | B: {fmt2(vb)} V | C: {fmt2(vc)} V | D Current: {fmt2(cd)} A"
        ]
        return ev

    def api(
        self, t_ms: int, raws: dict[int, int], mvs: dict[int, int] | None = None
    ) -> HttpResponse:
        """handleAPI(): re-reads the ADC and classifies those readings (not the last tick's)."""
        va, vb, vc, cd = readings(raws, mvs)
        status_ab = classify(min(va, vb))
        status_c = classify(vc)
        body = (
            "{"
            f'"PanelA_Voltage":{fmt2(va)},'
            f'"PanelB_Voltage":{fmt2(vb)},'
            f'"PanelC_Voltage":{fmt2(vc)},'
            f'"PanelD_Current":{fmt2(cd)},'
            f'"Status_PanelAB":"{status_ab}",'
            f'"Status_PanelC":"{status_c}",'
            f'"Status_PanelA":"{classify(va)}",'
            f'"Status_PanelB":"{classify(vb)}"'
            "}"
        )
        # server.sendHeader("Access-Control-Allow-Origin", "*") before server.send()
        return HttpResponse(200, "application/json", body, {"Access-Control-Allow-Origin": "*"})
