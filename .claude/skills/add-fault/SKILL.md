---
name: add-fault
description: Add a new fault type or failure mode to the solar-farm simulation harness (physics, sensor/ADC, or network level), with scenario, tests, control-panel support and coverage-report mapping. Use when asked to simulate a new kind of failure, degradation or transport problem.
---

# Add a fault to the harness

A fault is only done when all six steps below are done; the CLAUDE.md rule requires a scenario, a test and a coverage mapping for each one.

## 1. Choose the layer

| Layer | File | Applies to | Examples |
|---|---|---|---|
| Physics (what the panel really does) | `sim/physics.py`, in `Environment.panel()` | truth `V_*`, `I_D`, `/api/v2` panels | soiling, hot-spot, bypass-diode failure |
| Sensor / ADC (what the ESP32 reads) | `sim/adc.py`, in `to_raw()` | raw codes on GPIO 34/35/32/33 | drift, intermittent wire, divider tolerance |
| Network (what consumers receive) | `sim/emulator.py`, in the `network_faults` middleware | `/api`, `/api/v2` | partial response, slow drip, wrong content type |

## 2. Model it

* Physics and sensor faults:
  * add the kind to the `Literal[...]` in `Fault.kind` (`sim/config.py`) and document `value` there;
  * honour `f.active(t_s)` and `f.hits(target)`;
  * keep randomness on `adc._rng(sc, t_ms, pin)` or a `[seed, ...]`-keyed generator, so replay stays byte-identical.
* Network faults: add the mode to `Network.mode`.

## 3. Scenario

Add `sim/scenarios/<fault>.yaml` with a fixed seed, a short `duration_s`, and the fault in a time window so that before, during and after can all be asserted.

## 4. Tests

* Model-level: extend `sim/tests/test_physics_adc.py` (physics/ADC) or `sim/tests/test_emulator.py` (network).
* Consumer-level, if a consumer should react: add a Playwright case to `sim/tests/test_webui.py`, using `emulator(...)` and `control(srv, ...)`.
* Tag every test with `@pytest.mark.covers("FEAT-...", "HARN-SCEN")`. The IDs are in `sim/tests/conftest.py`.
* If the fault exposes a defect in the system under test, record it as `@pytest.mark.xfail(reason="F<next>: ...", strict=True)`. Add a row to the findings register in `docs/SIMULATION_HARNESS.md` and to the README findings table, then fix it with the `sut-fix-pr` skill.

## 5. Control panel

Expose it in `sim/static/control.html`. Panel faults go through `panelFaults()`; network modes go in the `#netMode` select. If it is user-facing, extend `test_control_panel.py`.

## 6. Verify and document

Run `uv run ruff check --fix sim && uv run ruff format sim && uv run pytest -q`, then check that `reports/coverage.md` maps the new tests. Add the fault to the fault-library table in `docs/SIMULATION_HARNESS.md`.
