---
name: run-scenario
description: Run a solar-farm simulation scenario with the harness, either live (emulator + control panel for index.html / UE) or accelerated (rig log CSV, Kaggle datasets). Use when asked to simulate a day or fault, reproduce a dashboard behaviour, generate test data, or demo the system without hardware.
---

# Run a simulation scenario

The scenarios live in `sim/scenarios/*.yaml`; the schema is `sim/config.py` (`Scenario`). List them with `ls sim/scenarios`.

## 1. Pick the mode

| Goal | Command |
|---|---|
| Live rig for `index.html`, the UE twin or a demo | `uv run python -m sim serve --scenario <name> [--backend fil] [--speed 10] [--port 8080]` |
| Telemetry log (one row per 2 s tick) | `uv run python -m sim generate rig --scenario <name> --out data/<name>.csv [--ticks N]` |
| ML notebook datasets | `uv run python -m sim generate kaggle --out data/kaggle --days 34 --inverters 22 --seed 42` |
| Real-time jitter check | `uv run python -m sim bench --seconds 60` |
| UE-style polling | `uv run python -m sim poll --url http://127.0.0.1:8080 --interval 2 --count 5` |

* Choose the backend:
  * `--backend fil` runs the real `Solar_Farm.ino` (compiled on first use into `build/fil/`). Use it whenever the question is about firmware behaviour.
  * The default `python` backend is the reference model. It is faster and identical by test.
* `serve` blocks. Run it in the background and stop it when you are done.

## 2. Drive it live

* Control panel: `http://127.0.0.1:<port>/control`.
* Scripted changes go through `POST /control` with JSON:
  * `{"irradiance_override": 0}` or `null`
  * `{"add_fault": {"kind": "disconnect", "target": "B"}}` or `{"faults": []}`
  * `{"network": {"mode": "hang"|"http_500"|"malformed_json"|"missing_keys"|"down"|"latency"|"ok", "latency_ms": 800, "cors": null|true|false}}`
  * `{"adc_model": "esp32", "acs_divider": false, "adc_noise_lsb": 3}`
* Inspect with `GET /api`, `/api/v2`, `/state` (truth, raw ADC, LEDs, Serial, Blynk), `/blynk/history?pin=0` and `/recording`.
* For the web UI: open `index.html` and enter `127.0.0.1:<port>` as the ESP32 IP.

## 3. New scenario

Copy the closest YAML, change `name` and `description`, and keep `seed` fixed for reproducibility. Then add it to the catalogue test: it is picked up automatically by `test_scenario_catalogue_runs_and_honours_contract`. Run `uv run pytest sim/tests/test_engine.py -q`.

## 4. Report

Quote the scenario name and seed, plus the backend you used. Give the key numbers: statuses, voltages and current, and any network errors. Quote the commands you ran so the result can be reproduced exactly.
