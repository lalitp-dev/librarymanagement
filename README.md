# 📚 Library Management System

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI%20UI-AC4FC6?style=for-the-badge)

**A full-stack library system with a beautiful terminal UI and a decoupled REST API backend.**

[Features](#-features) · [Tech Stack](#️-tech-stack) · [Installation](#-installation--setup) · [Running the App](#-running-the-application)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 **Beautiful CLI** | Color-coded, responsive terminal UI with formatted tables powered by `Rich` |
| 🔌 **RESTful API** | Fully decoupled architecture — client and server are completely independent |
| 🐘 **PostgreSQL Backend** | Secure, persistent data storage via SQLAlchemy ORM |
| 📖 **Core Operations** | View inventory, add books, borrow (with availability checks), and return books |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   CLI Frontend      ──▶   Flask API Backend     │
│   Python + Rich             Python + Flask      │
│   requests                  SQLAlchemy           │
│                                                 │
│                        ──▶   PostgreSQL DB       │
│                              psycopg2-binary     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Installation & Setup

> These instructions are for **Linux** (Debian/Ubuntu). Adjust package manager commands as needed for other distros.

### Step 1 — Install Prerequisites

```bash
sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib
```

### Step 2 — Clone & Set Up a Virtual Environment

```bash
# Clone the repository
git clone https://github.com/lalitp-dev/librarymanagement.git
cd library-management-system

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
pip install Flask Flask-SQLAlchemy psycopg2-binary requests rich
```

### Step 4 — Configure the Database

```bash
# Start the PostgreSQL service
sudo service postgresql start

# Switch to the postgres user and create the database
sudo -i -u postgres
createdb library_db
exit
```

> ⚙️ Update your database connection string in `app.py` if your PostgreSQL user or password differs from the defaults.

---

## ▶️ Running the Application

This project uses a **decoupled architecture** — the server and client run in separate terminals.

### Terminal 1 · Start the Backend Server

```bash
# Make sure your virtual environment is active
source venv/bin/activate

python app.py
```

The Flask API will start at `http://127.0.0.1:5000` and automatically create all required database tables on first run.

### Terminal 2 · Start the CLI Frontend

Open a **new terminal window**, navigate to the project directory, then:

```bash
source venv/bin/activate

python cli.py
```

You'll be greeted by the interactive, styled menu — start managing your library! 📖

---

## 📁 Project Structure

```
library-management-system/
├── app.py          # Flask API — routes, models, database logic
├── cli.py          # Rich CLI — interactive terminal frontend
└── README.md
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
