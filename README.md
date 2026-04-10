# 📚 AI Library Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-Web_UI-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI_UI-AC4FC6?style=for-the-badge)
![Groq AI](https://img.shields.io/badge/Groq_LPU-Llama_3.1-F55036?style=for-the-badge)

**A high-performance, AI-powered full-stack library system featuring a stunning web dashboard, a terminal UI, and a decoupled RESTful backend.**

[Features](#-features) · [Architecture](#️-architecture--tech-stack) · [Installation](#-installation--setup) · [Running the App](#-running-the-application)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Lightning AI Analysis** | Generates instantaneous, markdown-formatted book summaries using **Groq's Llama 3.1 8B** model, executing on specialized LPU hardware. |
| 🌐 **Stunning Web UI** | A completely responsive, glassmorphism-styled web dashboard featuring real-time analytics, debounced search filtering, and custom CSS animations. |
| 🛡️ **Failsafe Architecture** | Built-in **Presentation Fallback Protocols** instantly intercept 503 API traffic spikes and seamlessly serve cached local data to guarantee 100% uptime during live demos. |
| 🔌 **Multi-Client REST API** | A truly decoupled Flask backend that securely serves both a pure HTML/JS Web application and a Python Terminal application simultaneously. |
| 🎨 **Power-User CLI** | An alternative color-coded, responsive terminal interface built with `Rich` for developers who prefer keyboard-centric database management. |
| 🐘 **PostgreSQL Backend** | Secure, persistent relational data storage managed via the `SQLAlchemy` ORM. |
| 🔒 **Backend Security** | API keys and credentials are strictly isolated on the backend using `python-dotenv`. Frontends remain stateless and completely blind to security keys. |

---

## 🛠️ Architecture & Tech Stack

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│       Web Dashboard                  CLI Frontend            │
│  (HTML5 + Tailwind + JS)            (Python + Rich)          │
│             │                              │                 │
│             ▼                              ▼                 │
│      [ RESTful JSON HTTP Requests via CORS enabled API ]     │
│             │                              │                 │
│             └──────────────┬───────────────┘                 │
│                            ▼                                 │
│                    Flask API Backend                         │
│                    (Python + Flask)                          │
│                            │                                 │
│             ┌──────────────┴───────────────┐                 │
│             ▼                              ▼                 │
│          Groq API                    PostgreSQL DB           │
│   (Llama-3.1-8b-instant)            (SQLAlchemy ORM)         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation & Setup

### Step 1 — Install System Prerequisites

```bash
sudo pacman -S python python-pip postgresql
```

### Step 2 — Clone & Set Up a Virtual Environment

```bash
# Clone the repository
git clone https://github.com/lalitp-dev/librarymanagement.git
cd librarymanagement

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
pip install Flask Flask-SQLAlchemy flask-cors psycopg2-binary requests rich groq python-dotenv
```

### Step 4 — Configure the Database & Environment

**1. Start PostgreSQL & Create the Database**

```bash
# Start the PostgreSQL service
sudo systemctl start postgresql

# Switch to the postgres user and create the database
sudo -i -u postgres
createdb library_db
exit
```

> ⚙️ Update your database connection string in `app.py` if your PostgreSQL user or password differs from the defaults.

**2. Configure your API Keys**
Create a `.env` file in the root directory to store your Groq API key:

```bash
echo 'GROQ_API_KEY="gsk_your_actual_api_key_here"' > .env
```

---

## ▶️ Running the Application

Because this project utilizes a decoupled architecture, the backend server must be running to power the client interfaces.

### 1. Start the Backend Server

```bash
# Ensure your virtual environment is active
source venv/bin/activate

python app.py
```
The Flask API will start at `http://127.0.0.1:5000` and automatically create all required database tables on the first run. Keep this terminal running.

### 2. Launching the Frontends

You can interact with the system using either the Web Dashboard or the Terminal UI (or both simultaneously).

**Option A: The Web Dashboard (Recommended)**
Simply open the `index.html` file in any modern web browser (e.g., Chrome, Firefox, Brave). It will automatically connect to the local API.

**Option B: The CLI Application**
Open a **new terminal window**, navigate to the project directory, activate your virtual environment, and run:
```bash
source venv/bin/activate
python cli.py
```

---

## 📁 Project Structure

```text
librarymanagement/
├── .env            # Environment variables (Git ignored)
├── app.py          # Flask API — Routes, Models, AI logic, CORS
├── cli.py          # Rich CLI — Alternative terminal-based frontend
├── index.html      # Web UI — Glassmorphism dashboard & search engine
└── README.md       # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
