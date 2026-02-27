# 🛡️ NetWatch — Real-Time Network Monitoring & Anomaly Detection

A full-stack network monitoring platform that captures live traffic, stores packet metadata, and visualizes activity through an interactive dashboard with real-time anomaly detection.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Docker (Recommended)](#option-1--docker-recommended)
  - [Local Setup](#option-2--local-setup)
- [API Endpoints](#-api-endpoints)
- [Dashboard](#-dashboard)
- [License](#-license)

---

## ✨ Features

- **Live Packet Capture** — Sniffs network traffic in real time using Scapy (TCP, UDP, and other protocols)
- **Anomaly Detection** — Detects port scanning activity via threshold-based heuristics
- **Interactive Dashboard** — Auto-refreshing (every 2s) Streamlit dashboard with Plotly charts
- **Traffic Analytics** — Top talkers, protocol distribution, traffic-over-time trends
- **Alert System** — Real-time alerts for suspicious network behavior
- **Containerized** — Full Docker Compose setup for one-command deployment

---

## 🏗️ Architecture

```
┌─────────────┐      HTTP POST      ┌─────────────┐      SQL       ┌─────────────┐
│    Agent     │  ──────────────────▶│   Backend   │ ──────────────▶│ PostgreSQL  │
│  (Scapy)    │    /packets          │  (FastAPI)  │                │   Database  │
└─────────────┘                      └──────┬──────┘                └─────────────┘
                                            │
                                       HTTP GET
                                            │
                                     ┌──────▼──────┐
                                     │  Dashboard  │
                                     │ (Streamlit) │
                                     └─────────────┘
```

---

## 🛠️ Tech Stack

| Component   | Technology                     |
|-------------|--------------------------------|
| Agent       | Python, Scapy                  |
| Backend API | FastAPI, Uvicorn, SQLAlchemy   |
| Database    | PostgreSQL 16                  |
| Dashboard   | Streamlit, Plotly              |
| DevOps      | Docker, Docker Compose         |

---

## 📁 Project Structure

```
netwatch/
├── agent/
│   ├── Dockerfile
│   └── packet_sniffer.py        # Captures live network packets
├── backend/
│   ├── Dockerfile
│   ├── main.py                  # FastAPI application & routes
│   ├── models.py                # SQLAlchemy ORM models
│   ├── database.py              # Database connection config
│   └── detector.py              # Anomaly detection logic
├── dashboard/
│   ├── Dockerfile
│   └── app.py                   # Streamlit dashboard
├── docker-compose.yml           # Multi-container orchestration
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (for containerized setup)
- **Npcap** (Windows) or **libpcap** (Linux/Mac) for packet capture

---

### Option 1 — Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/MehdiElHarami/Network-Monitoring.git
cd Network-Monitoring

# Build and start all services
docker-compose up --build
```

| Service    | URL                          |
|------------|------------------------------|
| Dashboard  | http://localhost:8501         |
| Backend API| http://localhost:8000         |
| API Docs   | http://localhost:8000/docs    |

```bash
# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

### Option 2 — Local Setup

```bash
# Clone the repository
git clone https://github.com/MehdiElHarami/Network-Monitoring.git
cd Network-Monitoring

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

Run each service in a **separate terminal**:

```bash
# Terminal 1 — Backend
cd backend
uvicorn main:app --reload

# Terminal 2 — Agent (requires admin/root privileges)
cd agent
python packet_sniffer.py

# Terminal 3 — Dashboard
cd dashboard
streamlit run app.py
```

> **Note:** The agent requires administrator privileges to capture packets. Run your terminal as Admin (Windows) or use `sudo` (Linux/Mac).

---

## 📡 API Endpoints

| Method | Endpoint                    | Description                        |
|--------|-----------------------------|------------------------------------|
| POST   | `/packets`                  | Ingest a captured packet           |
| GET    | `/stats/summary`            | Total packets, unique IPs, traffic |
| GET    | `/stats/top-talkers`        | Top 5 source IPs by packet count   |
| GET    | `/stats/protocol-distribution` | Packet count per protocol       |
| GET    | `/stats/traffic-over-time`  | Traffic data for the last 30 min   |
| GET    | `/packets/recent?limit=30`  | Most recent captured packets       |
| GET    | `/alerts`                   | Active anomaly alerts              |

---

## 📊 Dashboard

The Streamlit dashboard includes:

- **Summary Metrics** — Total packets, unique sources/destinations, total traffic
- **Traffic Over Time** — Area chart showing packet volume in 30-second intervals
- **Protocol Distribution** — Donut chart breakdown (TCP / UDP / Other)
- **Top Talkers** — Bar chart of most active source IPs
- **Active Alerts** — Real-time port scanning detection alerts
- **Recent Packets** — Sortable table of the latest captured packets

Auto-refreshes every **2 seconds** for live monitoring.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
