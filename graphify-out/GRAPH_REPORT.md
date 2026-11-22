# Graph Report - Digital-Twin-Solar-Farm  (2026-11-22)

## Corpus Check
- 2 files · ~5,004 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .ipynb 1, .log 1)

## Summary
- 40 nodes · 44 edges · 7 communities (6 shown, 1 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `38e94056`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 🌞 Digital Twin Renewable Energy Solar Farm
- 🚀 Setup Instructions
- 🧠 Real-Time System Architecture
- 📥 System Inputs & Outputs
- sendData
- handleAPI

## God Nodes (most connected - your core abstractions)
1. `🌞 Digital Twin Renewable Energy Solar Farm` - 13 edges
2. `🚀 Setup Instructions` - 6 edges
3. `sendData()` - 5 edges
4. `🧠 Real-Time System Architecture` - 5 edges
5. `💻 Software Level (Firmware, Middleware & Applications)` - 5 edges
6. `readVoltage()` - 3 edges
7. `readCurrent()` - 3 edges
8. `handleAPI()` - 3 edges
9. `📥 System Inputs & Outputs` - 3 edges
10. `updateLEDs()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Tier 1 — Embedded Firmware (`Solar_Farm.ino`)` --references--> `sendData()`  [INFERRED]
  README.md → Solar_Farm.ino

## Import Cycles
- None detected.

## Communities (7 total, 1 thin omitted)

### Community 0 - "🌞 Digital Twin Renewable Energy Solar Farm"
Cohesion: 0.18
Nodes (10): 🎥 Demonstration Videos, 🌞 Digital Twin Renewable Energy Solar Farm, 🧩 How It Works, ⚙️ Key Features, 📄 License, 📘 Overview, 📈 Performance Log, 📂 Project Structure (+2 more)

### Community 1 - "🚀 Setup Instructions"
Cohesion: 0.33
Nodes (6): 1. Flash Firmware, 2. Configure Credentials, 3. Set Up Blynk Dashboard, 4. Open Local Web UI, 5. Connect Unreal Engine, 🚀 Setup Instructions

### Community 2 - "🧠 Real-Time System Architecture"
Cohesion: 0.25
Nodes (8): End-to-End Architecture Diagram, ⚡ Hardware Level (Physical Layer), 🧠 Real-Time System Architecture, 💻 Software Level (Firmware, Middleware & Applications), 🗄️ Storage Level (Data & Persistence), Tier 2 — Local Web Dashboard (`index.html`), Tier 3 — Unreal Engine 3D Digital Twin, Tier 4 — ML Analytics (`Untitled3.ipynb`)

### Community 4 - "📥 System Inputs & Outputs"
Cohesion: 0.67
Nodes (3): Inputs (Detailed), Outputs & Outcomes (Detailed), 📥 System Inputs & Outputs

### Community 5 - "sendData"
Cohesion: 0.67
Nodes (3): Tier 1 — Embedded Firmware (`Solar_Farm.ino`), sendData(), updateLEDs()

### Community 6 - "handleAPI"
Cohesion: 0.67
Nodes (3): handleAPI(), readCurrent(), readVoltage()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `🌞 Digital Twin Renewable Energy Solar Farm` connect `🌞 Digital Twin Renewable Energy Solar Farm` to `🚀 Setup Instructions`, `🧠 Real-Time System Architecture`, `📥 System Inputs & Outputs`?**
  _High betweenness centrality (0.719) - this node is a cross-community bridge._
- **Why does `🧠 Real-Time System Architecture` connect `🧠 Real-Time System Architecture` to `🌞 Digital Twin Renewable Energy Solar Farm`?**
  _High betweenness centrality (0.582) - this node is a cross-community bridge._
- **Why does `💻 Software Level (Firmware, Middleware & Applications)` connect `🧠 Real-Time System Architecture` to `sendData`?**
  _High betweenness centrality (0.538) - this node is a cross-community bridge._