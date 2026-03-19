# AI-Enabled Smart Energy Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ESP32-IoT%20Hardware-E7352C?style=for-the-badge&logo=espressif&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/MQTT-IoT%20Protocol-660066?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

> An intelligent IoT system that monitors real-time electricity consumption, predicts future usage, detects anomalies, and automatically controls loads — reducing energy wastage through AI-driven automation.

---

## 📌 Overview

AI-Enabled Smart Energy Management System is a complete end-to-end IoT solution for intelligent power monitoring and optimisation. ESP32 smart meters continuously measure voltage, current, and power consumption, streaming data to the cloud. An ML pipeline then predicts future consumption, detects anomalous usage patterns, and triggers automatic load control — cutting energy bills and carbon footprint.

---

## ✨ Features

- 🔌 **Real-time energy monitoring** — voltage, current, power factor, kWh tracking
- 📊 **Consumption analytics** — hourly, daily, monthly usage trends
- 🤖 **AI-based consumption prediction** — Random Forest forecasting
- 🚨 **Anomaly detection** — Isolation Forest flags unusual power spikes
- ⚡ **Automatic load control** — relay switching based on usage thresholds
- 🌐 **Remote dashboard** — live charts accessible from any browser
- 💰 **Cost estimation** — real-time electricity bill calculation
- 📱 **Alert system** — email + SMS on abnormal consumption

---

## 🏗️ System Architecture

```
[ESP32 Smart Meter]
    ├── PZEM-004T  → Voltage + Current + Power + kWh
    ├── ACS712     → Current sensing
    └── Relay      → Automatic load control
         ↓  (MQTT / HTTP)
[Cloud Storage — Firebase / InfluxDB]
         ↓
[ML Prediction Engine]
    ├── Random Forest    → Consumption forecasting
    ├── Isolation Forest → Anomaly detection
    └── Load Optimizer   → Auto control decisions
         ↓
[Flask Web Dashboard]
    ├── Live power charts
    ├── Usage analytics
    ├── Cost calculator
    └── Alert history
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| IoT Hardware | ESP32 + PZEM-004T + Relay Module |
| Firmware | Arduino C++ (ESP32) |
| Communication | MQTT + HTTP REST |
| Cloud Storage | Firebase / InfluxDB |
| ML Engine | Scikit-learn (Random Forest + Isolation Forest) |
| Backend | Flask (Python) |
| Frontend | HTML + CSS + Chart.js |
| Alerts | SMTP Email + Twilio SMS |

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Dashboard
```bash
git clone https://github.com/SAM-WESLEY/AI-Smart-Energy-Management
cd AI-Smart-Energy-Management
cp config.example.json config.json
python app.py
```

### Access Dashboard
```
http://localhost:5000
```

### Demo Mode (No Hardware Needed)
Click **⚡ Simulate** on the dashboard to generate live energy readings.

---

## 📊 Monitored Parameters

| Parameter | Unit | Description |
|---|---|---|
| Voltage | V | Supply voltage |
| Current | A | Load current draw |
| Active Power | W | Real power consumption |
| Power Factor | — | Efficiency ratio (0–1) |
| Energy | kWh | Cumulative consumption |
| Frequency | Hz | Supply frequency |

---

## 🚨 Alert Thresholds

| Condition | Threshold | Action |
|---|---|---|
| High consumption | >5 kW | Email + SMS alert |
| Voltage spike | >260V or <180V | Emergency relay cut |
| Anomaly detected | Isolation Forest flag | Notify admin |
| Daily budget exceeded | User-defined | Dashboard warning |

---

## 🗂️ Project Structure

```
AI-Smart-Energy-Management/
├── app.py                          # Main Flask application + monitor loop
├── config.example.json             # Firebase + MQTT + Alert credentials
├── modules/
│   ├── energy_monitor.py           # Real-time data fetcher + MQTT client
│   ├── ml_predictor.py             # Forecasting + anomaly detection
│   ├── load_controller.py          # Automatic relay / load control logic
│   └── alert_system.py             # Email + SMS alert system
├── esp32/
│   └── smart_meter.ino             # ESP32 firmware (PZEM-004T)
├── models/
│   └── energy_model.pkl            # Trained forecasting model
├── templates/
│   └── index.html                  # Live energy dashboard
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

---

## 🌍 Applications

- 🏠 Smart homes and apartments
- 🏭 Industrial energy saving and monitoring
- 🏢 Green buildings and smart offices
- ☀️ Solar + grid hybrid energy systems
- 🏥 Hospital power management

---

## 🔮 Future Scope

- ☀️ Solar panel output optimisation
- 🔋 Battery storage management
- 🌐 Smart grid integration
- 🤖 AI-based dynamic billing system
- 📱 Mobile app (Android / iOS)

---

## 📬 Contact

**Sam Wesley S**
📧 samwesley@karunya.edu.in
🔗 [LinkedIn](https://linkedin.com/in/samwesleys)
🐙 [GitHub](https://github.com/SAM-WESLEY)

---

<p align="center">
  <i>Built with ❤️ at Karunya Institute of Technology and Sciences</i>
</p>

<p align="center">If this project helped you, please give it a ⭐</p>
