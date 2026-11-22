# Graph Report - Digital-Twin-Solar-Farm  (2026-11-22)

## Corpus Check
- 52 files · ~22,522 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 5, .ipynb 1, .log 1)

## Summary
- 651 nodes · 1309 edges · 32 communities (28 shown, 4 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 114 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `439cdeab`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 🌞 Digital Twin Renewable Energy Solar Farm
- Scenario
- engine.py
- Solar Farm Digital Twin — Simulation & Verification Harness: Plan (Draft v1)
- Engine
- conftest.py
- json
- test_emulator.py
- test_webui.py
- emulator.py
- pytest
- steps
- WebServer
- shim.cpp
- String
- farm_n_panels.yaml
- panel_b_disconnect.yaml
- sensor_faults.yaml
- shading_and_degradation.yaml
- BlynkTimer
- cloudy_day.yaml
- lab_bench.yaml
- network_flaky.yaml
- BlynkWifi
- esp32_adc_physical.yaml
- WiFiClass
- clear_day.yaml
- night.yaml
- Digital-Twin-Solar-Farm + simulation harness
- Arduino.h
- main.cpp
- solar-twin-sim

## God Nodes (most connected - your core abstractions)
1. `Scenario` - 41 edges
2. `Engine` - 39 edges
3. `create_app()` - 21 edges
4. `WebServer` - 21 edges
5. `generate_kaggle()` - 20 edges
6. `Environment` - 17 edges
7. `FilFirmware` - 16 edges
8. `FirmwareModel` - 16 edges
9. `client()` - 16 edges
10. `check_v1_body()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `2. Components` --references--> `ServerThread`  [INFERRED]
  docs/SIMULATION_HARNESS.md → sim/emulator.py
- `Tier 1 — Embedded Firmware (`Solar_Farm.ino`)` --references--> `BlynkTimer`  [INFERRED]
  README.md → sim/fil/include/BlynkSimpleEsp32.h
- `2. Components` --references--> `Weather`  [INFERRED]
  docs/SIMULATION_HARNESS.md → sim/config.py
- `2. Components` --references--> `Fault`  [INFERRED]
  docs/SIMULATION_HARNESS.md → sim/config.py
- `2. Components` --references--> `Network`  [INFERRED]
  docs/SIMULATION_HARNESS.md → sim/config.py

## Import Cycles
- None detected.

## Communities (32 total, 4 thin omitted)

### Community 0 - "🌞 Digital Twin Renewable Energy Solar Farm"
Cohesion: 0.06
Nodes (31): 1. Flash Firmware, 2. Configure Credentials, 3. Set Up Blynk Dashboard, 4. Open Local Web UI, 5. Connect Unreal Engine, 🎥 Demonstration Videos, 🌞 Digital Twin Renewable Energy Solar Farm, End-to-End Architecture Diagram (+23 more)

### Community 1 - "Scenario"
Cohesion: 0.06
Nodes (33): 2. Components, Fault library, esp32_current_raw(), esp32_pin_raw(), esp32_voltage_raw(), ideal_current_raw(), ideal_voltage_raw(), _rng() (+25 more)

### Community 2 - "engine.py"
Cohesion: 0.09
Nodes (22): BlynkMock, BlynkWrite, make_backend(), FilFirmware, parse_events(), classify(), Events, FirmwareModel (+14 more)

### Community 3 - "Solar Farm Digital Twin — Simulation & Verification Harness: Plan (Draft v1)"
Cohesion: 0.08
Nodes (25): 1. Layered architecture, 3. Contracts, 4. Verification strategy, 5. Findings register, 6. Running it, 7. Assumptions and limits, Data flow per firmware tick, Simulation & Verification Harness: Architecture (+17 more)

### Community 4 - "Engine"
Cohesion: 0.08
Nodes (17): export_blynk_history(), generate_rig_log(), ServerThread, Clock, Engine, run(), TickRecord, emulator() (+9 more)

### Community 5 - "conftest.py"
Cohesion: 0.08
Nodes (9): build(), compiler(), FilError, FilProcess, FilTimeout, sketch_path(), fil_exe(), pytest_runtest_makereport() (+1 more)

### Community 6 - "json"
Cohesion: 0.11
Nodes (19): generate_kaggle(), _keys(), cmd_bench(), cmd_generate(), cmd_poll(), cmd_replay(), cmd_serve(), main() (+11 more)

### Community 7 - "test_emulator.py"
Cohesion: 0.15
Nodes (14): check_v1_body(), errors(), schema(), validate(), client(), test_api_cold_start_has_valid_status(), test_api_v1_contract(), test_api_v2_contract_and_panel_faults() (+6 more)

### Community 8 - "test_webui.py"
Cohesion: 0.19
Nodes (14): api(), test_control_panel_drives_emulator(), wait_api(), connect(), control(), test_ui_detects_hung_device(), test_ui_flags_bad_responses_as_disconnected(), test_ui_night_scenario_all_red() (+6 more)

### Community 9 - "emulator.py"
Cohesion: 0.10
Nodes (9): _cors(), create_app(), api(), api_v2(), blynk_connected(), blynk_get(), network_faults(), _token_ok() (+1 more)

### Community 10 - "pytest"
Cohesion: 0.15
Nodes (10): test_classification_boundaries(), test_current_formula_and_negative_clamp(), test_leds_one_hot_per_group(), test_tick_and_api_payload_format(), test_voltage_formula(), code(), data_dir(), test_notebook_r2_argument_order() (+2 more)

### Community 11 - "steps"
Cohesion: 0.11
Nodes (18): jobs, test, name, on, pull_request, push, branches, if (+10 more)

### Community 12 - "WebServer"
Cohesion: 0.14
Nodes (6): WebServer, headers_, pending_, port_, routes_, WebServer::handleClient()

### Community 13 - "shim.cpp"
Cohesion: 0.17
Nodes (6): HardwareSerial, digitalWrite(), emit(), flush_serial(), HardwareSerial::print(), HardwareSerial::printf()

### Community 14 - "String"
Cohesion: 0.17
Nodes (4): IPAddress, String, s, WebServer::send()

### Community 15 - "farm_n_panels.yaml"
Cohesion: 0.14
Nodes (13): description, duration_s, farm, n_panels, faults, kind, target, value (+5 more)

### Community 16 - "panel_b_disconnect.yaml"
Cohesion: 0.14
Nodes (13): description, duration_s, faults, kind, start_s, target, name, start (+5 more)

### Community 17 - "sensor_faults.yaml"
Cohesion: 0.15
Nodes (12): description, duration_s, faults, end_s, kind, start_s, target, value (+4 more)

### Community 18 - "shading_and_degradation.yaml"
Cohesion: 0.15
Nodes (12): description, duration_s, faults, end_s, kind, start_s, target, value (+4 more)

### Community 19 - "BlynkTimer"
Cohesion: 0.22
Nodes (6): BlynkTimer, T, interval, prev, timers_, millis()

### Community 20 - "cloudy_day.yaml"
Cohesion: 0.20
Nodes (9): adc_noise_lsb, description, duration_s, name, start, weather, cloud_model, cloud_persistence_s (+1 more)

### Community 21 - "lab_bench.yaml"
Cohesion: 0.20
Nodes (9): description, duration_s, name, start, weather, ambient_max_c, ambient_min_c, cloud_model (+1 more)

### Community 22 - "network_flaky.yaml"
Cohesion: 0.20
Nodes (9): description, duration_s, name, network, latency_ms, mode, start, weather (+1 more)

### Community 23 - "BlynkWifi"
Cohesion: 0.28
Nodes (3): BlynkWifi, configured_, delay()

### Community 24 - "esp32_adc_physical.yaml"
Cohesion: 0.22
Nodes (8): acs_divider, adc_model, description, duration_s, name, start, weather, cloud_model

### Community 26 - "clear_day.yaml"
Cohesion: 0.29
Nodes (6): description, duration_s, name, start, weather, cloud_model

### Community 27 - "night.yaml"
Cohesion: 0.29
Nodes (6): description, duration_s, name, start, weather, cloud_model

### Community 28 - "Digital-Twin-Solar-Farm + simulation harness"
Cohesion: 0.33
Nodes (5): Commands, Digital-Twin-Solar-Farm + simulation harness, graphify, Layout, Rules

## Knowledge Gaps
- **10 isolated node(s):** `solar-twin-sim`, `s`, `configured_`, `interval`, `prev` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 287 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Simulation & Verification Harness: Architecture` connect `Solar Farm Digital Twin — Simulation & Verification Harness: Plan (Draft v1)` to `Scenario`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Scenario` (e.g. with `2. Components` and `_rng()`) actually correct?**
  _`Scenario` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `solar-twin-sim`, `s`, `configured_` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `🌞 Digital Twin Renewable Energy Solar Farm` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Why does `2. Components` connect `Scenario` to `Solar Farm Digital Twin — Simulation & Verification Harness: Plan (Draft v1)`, `Engine`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `Engine` (e.g. with `export_blynk_history()` and `_cors()`) actually correct?**
  _`Engine` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Should `Scenario` be split into smaller, more focused modules?**
  _Cohesion score 0.05809802012333658 - nodes in this community are weakly interconnected._