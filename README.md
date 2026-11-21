# 🌞 Digital Twin Renewable Energy Solar Farm

> **Real-Time IoT Monitoring · Blynk Cloud · Unreal Engine 3D Digital Twin · Machine Learning Analytics**

An end-to-end IoT-driven smart monitoring system that captures real-time solar panel telemetry, pushes it to a cloud dashboard and a local web interface, and mirrors the physical solar farm as a fully interactive **3D Digital Twin** inside **Unreal Engine**.

---

## 📘 Table of Contents

- [Overview](#-overview)
- [Key Features](#️-key-features)
- [Real-Time System Architecture](#-real-time-system-architecture)
  - [End-to-End Architecture Diagram](#end-to-end-architecture-diagram)
  - [Hardware Level](#-hardware-level-physical-layer)
  - [Software Level](#-software-level-firmware-middleware--applications)
  - [Storage Level](#-storage-level-data--persistence)
- [System Inputs & Outputs](#-system-inputs--outputs)
- [Real-Time Data Flow & Sequence](#-real-time-data-flow--sequence)
- [Performance Log](#-performance-log)
- [Demonstration Videos](#-demonstration-videos)
- [How It Works](#-how-it-works)
- [Setup Instructions](#-setup-instructions)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## 📘 Overview

The **Digital Twin Renewable Energy Solar Farm** uses an **ESP32** microcontroller connected to **4 solar panels (6.9V each)**, voltage dividers, and an **ACS712 Hall-effect current sensor** to measure real-time electrical performance. The firmware processes sensor readings at a **2-second sampling interval**, classifies panel health into three states (Normal / Low / No Voltage), and simultaneously dispatches telemetry to:

1. **Blynk IoT Cloud** — remote dashboard with gauges, charts, and mobile alerts.
2. **Local REST API** (`GET /api`) — JSON endpoint served by the ESP32's on-chip web server.
3. **Local Web UI** (`index.html`) — glassmorphic browser dashboard polling the REST API.
4. **Unreal Engine 3D Digital Twin** — photorealistic virtual solar farm consuming the same REST API to drive dynamic materials, HUD overlays, and spatial inspection in real time.
5. **ML Analytics Pipeline** (Jupyter/Python) — offline linear regression models for yield forecasting and DC-to-AC efficiency estimation.

---

## ⚙️ Key Features

| Feature | Description |
| :--- | :--- |
| 🔋 **Real-Time Energy Monitoring** | Tracks individual panel voltage (A, B, C) and current (D) with 12-bit ADC resolution at 2 s intervals. |
| ☁️ **Blynk Cloud Dashboard** | Live gauges, trend graphs, and mobile push alerts via Virtual Pins V0–V5. |
| 🌐 **Local IP Web UI** | Responsive glassmorphic dashboard with async REST polling and virtual LED indicators. |
| 🚦 **Hardware LED Status** | 6 physical tri-color LEDs (2 groups × RGB) indicate panel health on the rig itself. |
| 🎮 **Unreal Engine 3D Digital Twin** | Interactive 3D virtual solar farm with dynamic material shaders, real-time HUD, and spatial inspection. |
| 📊 **ML Power Prediction** | Scikit-Learn linear regression forecasts AC output power from DC yield features (R² scoring). |
| 🔌 **REST JSON API** | Lightweight `/api` endpoint returns structured JSON for any external consumer. |

---

## 🧠 Real-Time System Architecture

### End-to-End Architecture Diagram

```mermaid
flowchart TD
    %% ── INPUT LAYER ──
    subgraph INPUT["🔽 INPUT LAYER"]
        direction TB
        SUN["☀️ Solar Irradiance"]
        CFG["⚙️ User Config\n(Wi-Fi SSID, Blynk Token, ESP IP)"]
        HTTP_REQ["🌐 HTTP GET /api Requests\n(Web UI · Unreal Engine)"]
    end

    %% ── HARDWARE LAYER ──
    subgraph HARDWARE["⚡ HARDWARE LEVEL — Physical Layer"]
        direction TB
        subgraph PANELS["Solar Panel Array — 4 × 6.9 V"]
            PA["Panel A\n(Voltage)"]
            PB["Panel B\n(Voltage)"]
            PC["Panel C\n(Voltage)"]
            PD["Panel D\n(Current)"]
        end

        subgraph SENSORS["Sensor Module"]
            VS_A["Voltage Divider A\nGPIO 34"]
            VS_B["Voltage Divider B\nGPIO 35"]
            VS_C["Voltage Divider C\nGPIO 32"]
            CS_D["ACS712 5A Sensor\nGPIO 33"]
        end

        subgraph ESP32["ESP32 Microcontroller"]
            ADC["12-bit SAR ADC\n(0 – 4095)"]
            CPU["Dual-Core Xtensa LX6\nFirmware Engine"]
            WIFI["Wi-Fi 802.11 b/g/n\nRadio"]
        end

        subgraph LEDS["Physical LED Indicators"]
            LED_AB["LED Group AB\nR:14 Y:12 G:13"]
            LED_CD["LED Group CD\nR:25 Y:26 G:27"]
        end
    end

    %% ── SOFTWARE LAYER ──
    subgraph SOFTWARE["💻 SOFTWARE LEVEL — Firmware, Middleware & Applications"]
        direction TB
        subgraph FW["Embedded Firmware — Solar_Farm.ino"]
            SAMPLE["Signal Sampling &\nCalibration"]
            STATE["Threshold State Engine\n(≤1V Red · <5V Yellow · ≥5V Green)"]
            TIMER["BlynkTimer\n(2000 ms cycle)"]
            WEBSVR["WebServer :80\nREST /api"]
        end

        subgraph WEBUI["Local Web UI — index.html"]
            POLL["Async Fetch Poller\n(2000 ms)"]
            RENDER["Glassmorphism Dashboard\n& Virtual LED Display"]
        end

        subgraph UE["Unreal Engine — 3D Digital Twin"]
            UE_REST["HTTP / VaRest\nBlueprint Client"]
            UE_WORLD["3D Solar Farm\nVirtual Environment"]
            UE_MAT["Dynamic Material\n& State Shaders"]
            UE_HUD["Spatial HUD &\nTelemetry Overlay"]
        end

        subgraph ML["Analytics & ML — Jupyter Notebook"]
            LR["Linear Regression\nPower Predictor"]
            EFF["AC/DC Efficiency\nEstimator"]
        end
    end

    %% ── STORAGE LAYER ──
    subgraph STORAGE["🗄️ STORAGE LEVEL — Persistence"]
        direction TB
        SRAM["ESP32 SRAM\n(Runtime Buffers)"]
        FLASH["ESP32 Flash\n(Firmware Binary)"]
        LS["Browser localStorage\n(Saved ESP IP)"]
        BLYNK_DB["Blynk Cloud\nTimeseries Store\n(V0–V5)"]
        CSV["CSV Datasets\n(Google Drive)"]
    end

    %% ── OUTPUT LAYER ──
    subgraph OUTPUT["📤 OUTPUT & OUTCOME LAYER"]
        direction TB
        OUT_LED["🚦 Physical LEDs\n(Hardware Status)"]
        OUT_SERIAL["🖥️ Serial Monitor\n(115200 baud Debug)"]
        OUT_JSON["📡 JSON REST Payload"]
        OUT_BLYNK["☁️ Blynk Mobile &\nWeb Dashboard"]
        OUT_WEB["🌐 Local Web UI\nReal-Time Metrics"]
        OUT_3D["🎮 Unreal Engine\n3D Virtual Twin"]
        OUT_ML["📈 ML Predictions\n(Yield & Efficiency)"]
    end

    %% ── CONNECTIONS ──
    SUN --> PANELS
    CFG -.-> ESP32
    HTTP_REQ -.-> WEBSVR

    PA --> VS_A
    PB --> VS_B
    PC --> VS_C
    PD --> CS_D

    VS_A -->|"Analog 0–10 V"| ADC
    VS_B -->|"Analog 0–10 V"| ADC
    VS_C -->|"Analog 0–10 V"| ADC
    CS_D -->|"Analog 0–5 V"| ADC

    ADC --> CPU
    CPU <--> SRAM
    CPU --> SAMPLE --> STATE

    STATE -->|"GPIO Write"| LEDS
    LEDS --> OUT_LED

    STATE -->|"Serial.printf"| OUT_SERIAL
    STATE --> WEBSVR
    TIMER -->|"VirtualWrite V0–V5"| WIFI

    WIFI -->|"Blynk Protocol"| BLYNK_DB
    BLYNK_DB --> OUT_BLYNK

    WEBSVR -->|"HTTP 200 JSON"| OUT_JSON
    OUT_JSON --> POLL
    POLL --> RENDER
    LS <--> WEBUI
    RENDER --> OUT_WEB

    OUT_JSON --> UE_REST
    UE_REST --> UE_MAT & UE_HUD
    UE_MAT & UE_HUD --> UE_WORLD
    UE_WORLD --> OUT_3D

    CSV --> ML
    ML --> OUT_ML

    CPU -.-> FLASH
```

---

### ⚡ Hardware Level (Physical Layer)

| # | Component | Specification | Pin / Interface | Role |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Solar Panel A** | 6.9 V PV (Parallel with B) | Analog node → Voltage Divider | Voltage source for monitoring group AB. |
| 2 | **Solar Panel B** | 6.9 V PV (Parallel with A) | Analog node → Voltage Divider | Voltage source for monitoring group AB. |
| 3 | **Solar Panel C** | 6.9 V PV (Series with D) | Analog node → Voltage Divider | Voltage source for monitoring group CD. |
| 4 | **Solar Panel D** | 6.9 V PV (Series with C) | Analog node → ACS712 | Current source measured by Hall-effect sensor. |
| 5 | **Voltage Sensor A** | Resistive voltage divider (0–10 V input) | `GPIO 34` — ADC1_CH6 | Scales panel voltage to 0–3.3 V for ADC. |
| 6 | **Voltage Sensor B** | Resistive voltage divider (0–10 V input) | `GPIO 35` — ADC1_CH7 | Scales panel voltage to 0–3.3 V for ADC. |
| 7 | **Voltage Sensor C** | Resistive voltage divider (0–10 V input) | `GPIO 32` — ADC1_CH4 | Scales panel voltage to 0–3.3 V for ADC. |
| 8 | **Current Sensor D** | ACS712-05B (5 A, 185 mV/A, 2.5 V offset) | `GPIO 33` — ADC1_CH5 | Measures DC current via Hall effect. |
| 9 | **ESP32** | Espressif Dual-Core Xtensa LX6, 240 MHz, 520 KB SRAM, 4 MB Flash | SoC | Edge processing, Wi-Fi, web server, Blynk client. |
| 10 | **LED Group AB** | 3 × 5 mm LEDs (Red, Yellow, Green) | `R:14` `Y:12` `G:13` | Physical status for Panels A + B combined. |
| 11 | **LED Group CD** | 3 × 5 mm LEDs (Red, Yellow, Green) | `R:25` `Y:26` `G:27` | Physical status for Panel C (and D context). |

**Panel Wiring Configuration:**

| Group | Panels | Connection | Purpose |
| :---: | :---: | :--- | :--- |
| AB | A + B | **Parallel** | Combined voltage monitoring — average of two panels. |
| CD | C + D | **Series** | Current measurement and flow control. |

---

### 💻 Software Level (Firmware, Middleware & Applications)

```mermaid
flowchart LR
    subgraph T1["Tier 1 — Embedded Firmware"]
        A1["Arduino Core for ESP32"]
        A2["ADC Signal Processing"]
        A3["State Classification\n(3-state threshold)"]
        A4["WebServer + Blynk Client"]
    end

    subgraph T2["Tier 2 — Local Web Dashboard"]
        B1["HTML5 / CSS3\nGlassmorphism UI"]
        B2["Vanilla JS\nAsync Fetch Client"]
    end

    subgraph T3["Tier 3 — 3D Digital Twin"]
        C1["Unreal Engine 4/5"]
        C2["HTTP REST Blueprint"]
        C3["Parameterized Shaders"]
        C4["Spatial Simulation"]
    end

    subgraph T4["Tier 4 — ML Analytics"]
        D1["Jupyter / Python"]
        D2["Scikit-Learn LR"]
        D3["Efficiency Modeling"]
    end

    T1 -->|"JSON /api"| T2
    T1 -->|"JSON /api"| T3
    T1 -->|"Blynk Cloud"| T3
    T4 -.->|"Offline Insights"| T3
```

#### Tier 1 — Embedded Firmware (`Solar_Farm.ino`)

**Signal Calibration Formulas:**

| Measurement | Formula | Notes |
| :--- | :--- | :--- |
| **Voltage** | `V = (raw / 4095.0) × 10.0` | 12-bit ADC, 10 V full-scale via voltage divider. |
| **Current** | `I = ((raw / 4095.0) × 5.0 − 2.5) / 0.185` | ACS712 5A: 185 mV/A sensitivity, 2.5 V zero offset. Negative clamped to 0. |

**Three-State Health Classification:**

| State | Condition | LED Color | Status String |
| :---: | :--- | :---: | :--- |
| 🔴 Critical | Avg voltage ≤ 1.0 V | **Red** | `RED: No Voltage` |
| 🟡 Warning | 1.0 V < voltage < 5.0 V | **Yellow** | `YELLOW: Low Voltage` |
| 🟢 Normal | Voltage ≥ 5.0 V | **Green** | `GREEN: Normal` |

**Communication Channels:**

| Channel | Protocol | Target | Interval |
| :--- | :--- | :--- | :--- |
| Blynk Cloud | Blynk protocol over TCP/SSL | Virtual Pins V0–V5 | 2000 ms (non-blocking `BlynkTimer`) |
| REST API | HTTP/1.1 `GET /api` | Any HTTP client | On-demand (request–response) |
| Serial Debug | UART 115200 baud | Arduino Serial Monitor | 2000 ms (with `sendData()`) |

**API Response Schema:**

```json
{
  "PanelA_Voltage": 6.85,
  "PanelB_Voltage": 6.80,
  "PanelC_Voltage": 6.78,
  "PanelD_Current": 1.25,
  "Status_PanelAB": "GREEN: Normal",
  "Status_PanelC": "GREEN: Normal"
}
```

#### Tier 2 — Local Web Dashboard (`index.html`)

- **Tech Stack:** HTML5, CSS3 (glassmorphism, backdrop blur, animations), vanilla JavaScript.
- **Data Acquisition:** `fetch()` polling `http://<espIP>/api` every 2000 ms.
- **Display:** Real-time voltage/current metrics, software LED circles (Red/Yellow/Green/Off), connection status indicator, configurable ESP32 IP field persisted in `localStorage`.

#### Tier 3 — Unreal Engine 3D Digital Twin

| Component | Implementation | Purpose |
| :--- | :--- | :--- |
| **Data Ingestion** | HTTP GET via VaRest plugin or UE HTTP module (Blueprints/C++) | Fetches JSON from ESP32 `/api` endpoint. |
| **3D Environment** | Photorealistic solar array, terrain, skybox with directional sun | Immersive virtual replica of the physical farm. |
| **Dynamic Materials** | Parameterized material instances driven by telemetry state | Panels shift emissive color (Green → Yellow → Red) in real time. |
| **Telemetry HUD** | UMG widget blueprints anchored to 3D panel actors | Floating voltage/current labels on each virtual panel. |
| **Spatial Inspection** | Free-fly and orbit camera with click-to-inspect | Users can navigate and query any panel in 3D space. |

#### Tier 4 — ML Analytics (`Untitled3.ipynb`)

- **Data Sources:** `Plant_2_Generation_Data.csv` (historical solar generation records).
- **Pipeline:** Pandas data processing → Seaborn/Matplotlib visualization → Scikit-Learn modeling.
- **Models:** Linear Regression forecasting `AC_POWER` from multi-variate DC features (`DC_POWER`, `DAILY_YIELD`, `TOTAL_YIELD`).
- **Metrics:** R² score, output power vs. efficiency curves.

---

### 🗄️ Storage Level (Data & Persistence)

| Layer | Type | Technology | Data | Retention |
| :--- | :--- | :--- | :--- | :--- |
| **Edge RAM** | Volatile | ESP32 SRAM (520 KB) | Live sensor readings, JSON buffers, TCP sockets | Cleared on reboot |
| **Edge Flash** | Non-Volatile | ESP32 SPI Flash (4 MB) | Compiled firmware, bootloader, Wi-Fi creds | Persistent across reboots |
| **Client** | Local | Browser `localStorage` | Saved ESP32 IP address | Per-browser persistent |
| **Cloud** | Time-Series | Blynk IoT Cloud DB | V0–V5 historical telemetry, device state | Cloud-tier dependent |
| **Offline** | File | CSV / Google Drive | Plant generation data, weather metrics | Long-term archival |

---

## 📥 System Inputs & Outputs

```mermaid
flowchart LR
    subgraph INPUTS["📥 INPUTS"]
        direction TB
        I1["☀️ Solar Irradiance"]
        I2["⚡ Analog Voltage (GPIO 34, 35, 32)"]
        I3["🔌 Analog Current (GPIO 33)"]
        I4["🔑 Wi-Fi + Blynk Credentials"]
        I5["🌐 HTTP GET /api Requests"]
        I6["📁 Historical CSV Datasets"]
    end

    subgraph CORE["🧠 PROCESSING CORE"]
        direction TB
        C1["Signal Acquisition"]
        C2["Health Classification"]
        C3["Telemetry Dispatch"]
        C4["3D Twin Rendering"]
        C5["ML Forecasting"]
    end

    subgraph OUTPUTS["📤 OUTPUTS & OUTCOMES"]
        direction TB
        O1["🚦 Physical LED Status"]
        O2["🖥️ Serial Debug Stream"]
        O3["📡 REST JSON Payload"]
        O4["☁️ Blynk Cloud Dashboard"]
        O5["🌐 Local Web UI"]
        O6["🎮 UE 3D Digital Twin"]
        O7["📈 ML Yield Predictions"]
    end

    INPUTS --> CORE --> OUTPUTS
```

### Inputs (Detailed)

| # | Input | Source | Type | Description |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Solar Irradiance | Environment | Physical | Sunlight incident on the 4 solar panels. |
| 2 | Panel A Voltage | Voltage Divider → GPIO 34 | Analog (0–3.3 V) | Scaled representation of Panel A's 0–10 V output. |
| 3 | Panel B Voltage | Voltage Divider → GPIO 35 | Analog (0–3.3 V) | Scaled representation of Panel B's 0–10 V output. |
| 4 | Panel C Voltage | Voltage Divider → GPIO 32 | Analog (0–3.3 V) | Scaled representation of Panel C's 0–10 V output. |
| 5 | Panel D Current | ACS712 → GPIO 33 | Analog (0–5 V) | Hall-effect current measurement of series string. |
| 6 | Wi-Fi Credentials | Firmware constants | Config | SSID and password for network connectivity. |
| 7 | Blynk Auth Token | Firmware constants | Config | Authentication for Blynk cloud platform. |
| 8 | ESP32 IP Address | Web UI text field | Config | Target IP for REST API polling. |
| 9 | HTTP Requests | Web UI / Unreal Engine | Network | `GET /api` calls triggering JSON response. |
| 10 | CSV Datasets | Google Drive / Local | File | Historical generation and weather data for ML training. |

### Outputs & Outcomes (Detailed)

| # | Output | Destination | Format | Description |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **LED Status** | Physical rig | GPIO HIGH/LOW | 6 LEDs show real-time Red/Yellow/Green state per panel group. |
| 2 | **Serial Log** | Arduino IDE Monitor | UART text | `A: 6.85 V \| B: 6.80 V \| C: 6.78 V \| D Current: 1.25 A` |
| 3 | **JSON Payload** | HTTP clients | `application/json` | Structured telemetry with voltages, current, status strings. |
| 4 | **Blynk Dashboard** | Mobile & Web app | Blynk widgets | Live gauges, charts, trend history, and push notifications. |
| 5 | **Local Web UI** | Browser | HTML/CSS/JS | Glassmorphic metrics, virtual LEDs, connection indicator. |
| 6 | **UE 3D Digital Twin** | Unreal Engine viewport | 3D render | Virtual panels change material color, floating HUD with live telemetry. |
| 7 | **ML Predictions** | Jupyter output | Plots & scores | R² accuracy, power vs. efficiency curves, yield forecasts. |

---

## 🔄 Real-Time Data Flow & Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Sun as ☀️ Solar Irradiance
    participant Panels as 🔋 Panels A–D & Sensors
    participant ESP as 🧠 ESP32 Firmware
    participant LEDs as 🚦 Physical LEDs
    participant Blynk as ☁️ Blynk Cloud
    participant Web as 🌐 Web UI (index.html)
    participant UE as 🎮 Unreal Engine 3D Twin

    Sun->>Panels: Illuminates 4 × 6.9V panels
    Panels->>ESP: Analog signals (GPIO 34, 35, 32, 33)

    Note over ESP: ADC Read → Calibration<br/>V = (raw/4095) × 10.0<br/>I = ((raw/4095)×5.0 − 2.5) / 0.185

    Note over ESP: State Classification<br/>≤1.0V → RED | <5.0V → YELLOW | ≥5.0V → GREEN

    ESP->>LEDs: GPIO Write (Pins 14,12,13 & 25,26,27)

    rect rgb(40, 60, 100)
        Note over ESP,UE: Parallel Real-Time Dispatch (every 2000 ms)

        ESP->>Blynk: Blynk.virtualWrite(V0–V5)
        Blynk-->>Blynk: Update mobile & web gauges

        Web->>ESP: HTTP GET /api
        ESP-->>Web: 200 OK — JSON payload
        Web-->>Web: Update DOM, virtual LEDs, timestamps

        UE->>ESP: HTTP GET /api
        ESP-->>UE: 200 OK — JSON payload
        UE-->>UE: Update 3D materials, HUD, sun vector
    end
```

---

## 📈 Performance Log

> Detailed system performance benchmarks are tracked in [`performance.log`](./performance.log).

**Key Metrics Summary:**

| Metric | Value |
| :--- | :--- |
| Firmware Sampling Interval | 2000 ms |
| ADC Resolution | 12-bit (4096 levels) |
| Voltage Measurement Precision | ±0.0024 V (10.0 V / 4095) |
| Current Measurement Precision | ±0.0066 A (1.22 mV / 0.185) |
| REST API Response Size | ~180–220 bytes |
| REST API Latency (LAN) | < 15 ms |
| Blynk Cloud Latency | ~50–200 ms (network dependent) |
| Web UI Polling Cycle | 2000 ms |
| Unreal Engine Polling Cycle | Configurable (1000–5000 ms typical) |
| ESP32 Firmware Flash Size | ~750 KB (compiled) |
| ESP32 Free Heap (Runtime) | ~180–220 KB |
| Concurrent HTTP Clients | 4–8 (ESP32 WebServer limit) |
| Wi-Fi Standard | 802.11 b/g/n (2.4 GHz) |

---

## 🎥 Demonstration Videos

| Feature | Video | Description |
| :--- | :--- | :--- |
| 🌤️ Full Project Demo | [`Digital Twin Solar Farm.mp4`](./Digital%20Twin%20Solar%20Farm.mp4) | Complete overview — sensors, dashboard, and monitoring. |
| ☁️ Blynk Cloud Dashboard | [`BLYNK.mov`](./BLYNK.mov) | Live solar panel performance via Blynk IoT Cloud. |
| 🌐 Local IP Dashboard | [`IP Web UI.mp4`](./IP%20Web%20UI.mp4) | Local ESP-based web monitoring interface demo. |
| 🧠 Digital Twin Dashboard | [`Solar Farm Dashboard.mp4`](./Solar%20Farm%20Dashboard.mp4) | Digital twin visualization and real-time analytics. |
| 🎮 UE 3D Simulation | [🔗 Google Drive](https://drive.google.com/file/d/1ea5y91UBZI5iZVrHjFSSdWAlmYECj8rJ/view?usp=sharing) | Interactive 3D Unreal Engine Digital Twin simulation. |

---

## 🧩 How It Works

```
  ┌────────────┐     Analog      ┌──────────┐    Wi-Fi     ┌──────────────┐
  │  4 × Solar │───── Signals ──▶│  ESP32   │────────────▶│ Blynk Cloud  │
  │   Panels   │    (V & I)      │ Firmware │             │  Dashboard   │
  └────────────┘                 └────┬─┬───┘             └──────────────┘
                                      │ │
                          ┌───────────┘ └──────────────┐
                          ▼                            ▼
                   ┌──────────────┐           ┌────────────────┐
                   │  Local Web   │           │ Unreal Engine  │
                   │   UI (HTML)  │           │  3D Twin (UE5) │
                   │ GET /api     │           │  GET /api      │
                   └──────────────┘           └────────────────┘
```

1. **Data Collection:** Voltage dividers and the ACS712 sensor feed analog signals from Panels A–D into the ESP32's 12-bit ADC channels.
2. **Processing & Classification:** The firmware reads ADC values, applies calibration formulas, classifies panel health into Red/Yellow/Green, and actuates physical LEDs.
3. **Telemetry Dispatch:** Processed data is sent to Blynk Cloud (every 2 s), served as JSON on `GET /api`, and printed to the serial monitor.
4. **Digital Twin Sync:** Both the local web dashboard and the Unreal Engine 3D environment poll `GET /api` to keep their virtual representations synchronized with the physical solar farm.
5. **ML Analytics:** Historical generation data is analyzed offline in Jupyter to build predictive models for yield forecasting and efficiency estimation.

---

## 🚀 Setup Instructions

### 1. Flash Firmware

```bash
# Open Solar_Farm.ino in Arduino IDE
# Select Board: ESP32 Dev Module
# Select Port: /dev/cu.usbserial-XXXX (macOS) or COMx (Windows)
# Click Upload
```

### 2. Configure Credentials

Update these constants in `Solar_Farm.ino`:

```cpp
#define BLYNK_TEMPLATE_ID   "Your_Template_ID"
#define BLYNK_AUTH_TOKEN     "Your_Auth_Token"

char ssid[] = "Your_WiFi_SSID";
char pass[] = "Your_WiFi_Password";
```

### 3. Set Up Blynk Dashboard

- Create a new template named **Solar Farm** on [blynk.cloud](https://blynk.cloud).
- Add 6 Datastreams mapped to Virtual Pins `V0`–`V5`.
- Design your dashboard with gauge and label widgets.

### 4. Open Local Web UI

- After ESP32 connects to Wi-Fi, note the IP from the Serial Monitor.
- Open `index.html` in a browser and enter the ESP32 IP address.

### 5. Connect Unreal Engine

- Import VaRest plugin (or use built-in HTTP module).
- Create an HTTP GET Blueprint targeting `http://<ESP32_IP>/api`.
- Parse JSON and bind values to material parameters and HUD widgets.

---

## 📂 Project Structure

```
Digital-Twin-Solar-Farm-main/
├── Solar_Farm.ino              # ESP32 firmware (sensor processing, Blynk, REST API)
├── index.html                  # Local glassmorphic web dashboard
├── Untitled3.ipynb             # Jupyter ML notebook (Linear Regression, efficiency)
├── performance.log             # System performance benchmarks & metrics
├── README.md                   # This architecture documentation
├── Digital Twin Solar Farm.mp4 # Full project demo video
├── BLYNK.mov                   # Blynk cloud dashboard demo
├── IP Web UI.mp4               # Local web UI demo
├── Solar Farm Dashboard.mp4    # Digital twin dashboard demo
└── Ip Web UI                   # Legacy placeholder file
```

---

## 📄 License

This project is for educational and research purposes.

---

<p align="center">
  <b>Built with ❤️ by Vishnu</b><br/>
  <i>ESP32 · Blynk IoT · Unreal Engine · Scikit-Learn</i>
</p>
