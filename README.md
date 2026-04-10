Here is the completely revamped `README.md`. It highlights the new AI capabilities, the robust retry logic, the complete CRUD architecture, and the secure environment variable handling.

The installation instructions have also been updated to utilize `pacman` and `systemctl` for a smoother setup in your local environment.

-----

````markdown
# 📚 Library Management System

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-CLI%20UI-AC4FC6?style=for-the-badge)
![Gemini AI](https://img.shields.io/badge/Gemini_2.5_Flash-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)

**A highly resilient, AI-powered full-stack library system featuring a beautifully formatted terminal UI and a decoupled RESTful backend.**

[Features](#-features) · [Tech Stack](#️-tech-stack) · [Installation](#-installation--setup) · [Running the App](#-running-the-application)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI-Powered Summaries** | Instantly generate concise, markdown-formatted book summaries directly in the terminal using the **Gemini 2.5 Flash** model. |
| 🛡️ **Resilient Architecture** | Built-in **Exponential Backoff & Retry Logic** automatically handles 503 API congestion and network spikes without crashing. |
| 🎨 **Stunning CLI UI** | Color-coded, responsive terminal interface with auto-formatting tables and loading spinners powered by `Rich`. |
| 🔌 **Decoupled REST API** | Client and server run entirely independently, communicating via lightweight JSON HTTP requests. |
| 🐘 **PostgreSQL Backend** | Secure, persistent data storage via the `SQLAlchemy` ORM. |
| ⚙️ **Secure Configuration** | API keys and credentials are safely isolated and autoloaded using `python-dotenv`. |
| 📖 **Full CRUD Lifecycle** | Complete database operations: Add, View, Borrow (with availability constraints), Return, and securely Remove books. |

---

## 🛠️ Tech Stack

```text
┌────────────────────────────────────────────────────────┐
│                                                        │
│     CLI Frontend             Flask API Backend         │
│     (Python + Rich)          (Python + Flask)          │
│            │                         │                 │
│            ▼                         ▼                 │
│       Gemini API               PostgreSQL DB           │
│   (google-genai SDK)          (SQLAlchemy ORM)         │
│                                                        │
└────────────────────────────────────────────────────────┘
````

-----

## 🚀 Installation & Setup

### Step 1 — Install System Prerequisites

```bash
sudo pacman -S python python-pip postgresql
```

### Step 2 — Clone & Set Up a Virtual Environment

```bash
# Clone the repository
git clone [https://github.com/lalitp-dev/librarymanagement.git](https://github.com/lalitp-dev/librarymanagement.git)
cd librarymanagement

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
pip install Flask Flask-SQLAlchemy psycopg2-binary requests rich google-genai python-dotenv
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
Create a `.env` file in the root directory to store your Gemini API key:

```bash
echo 'GEMINI_API_KEY="your_actual_api_key_here"' > .env
```

-----

## ▶️ Running the Application

This project uses a **decoupled architecture** — the server and client run in separate terminal instances.

### Terminal 1 · Start the Backend Server

```bash
# Ensure your virtual environment is active
source venv/bin/activate

python app.py
```

The Flask API will start at `http://127.0.0.1:5000` and automatically create all required database tables on the first run.

### Terminal 2 · Start the CLI Frontend

Open a **new terminal window**, navigate to the project directory, and start the client:

```bash
source venv/bin/activate

python cli.py
```

You'll be greeted by the interactive, styled menu. You can now manage your inventory and query the AI\! 📖

-----

## 📁 Project Structure

```text
librarymanagement/
├── .env            # Environment variables (Git ignored)
├── app.py          # Flask API — routes, models, database logic
├── cli.py          # Rich CLI — interactive frontend, AI integration, retry logic
└── README.md       # Project documentation
```

-----

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```
```
