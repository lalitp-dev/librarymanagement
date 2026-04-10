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
