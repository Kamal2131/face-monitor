# Face Monitor Proctoring System

_A browser-based exam proctoring application built with FastAPI, SQLAlchemy, and face-api.js for real-time face recognition and anti-cheat monitoring._

> **Note**  
> This system allows administrators to manage exams and students, while monitoring user activity to prevent cheating during online assessments.

---

## 📑 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
    - [Admin Dashboard](#admin-dashboard)
    - [Student Module](#student-module)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Features

- **Real-time Face Recognition:**  
    Uses `face-api.js` for detecting and verifying faces via webcam.

- **Anti-tab Switch Detection:**  
    Tracks browser tab changes to log suspicious behavior.

- **Exam Session Management:**  
    Admins can create user and delete user.

- **User Role Management:**  
    Separate dashboards for admin and student roles.

- **Event Logging:**  
    Logs face verification attempts, tab switches, and other actions.

- **Notifications & Alerts:**  
    Sends real-time alerts for suspicious activity.

---

## 🏗️ Architecture

```mermaid
graph LR
    A[Client (Browser)] -- face-api.js --> B[FastAPI Server]
    B -- SQLAlchemy ORM --> C[SQLite Database]
```

- **Client:**  
    Built with HTML/CSS/JS and `face-api.js` models for face detection.  
    Periodically sends monitoring events to the FastAPI backend.

- **Backend:**  
    FastAPI for RESTful API endpoints.  
    SQLAlchemy models for User, Exam, FaceLog, TabEvent, etc.  
    Role-based access control via JWT or cookie-based authentication.

- **Database:**  
    SQLite3 by default (configurable for Postgres/MySQL).

---

## 🏁 Getting Started

### Prerequisites

- Python 3.9+
- Node.js (for front-end dev servers, if applicable)
- Git

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Kamal2131/face-monitor.git
cd face-monitor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## 🛠️ Configuration

Copy the example environment file and customize:

```bash
cp .env.example .env
# Edit .env to set SECRET_KEY, DATABASE_URL, etc.
```

---

## 🗄️ Database Setup

Run migrations or create tables:

```bash
# If using Alembic:
alembic upgrade head

# Or directly from Python:
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧑‍💼 Usage

### Admin Dashboard

- **Login:** Navigate to `/login` and authenticate as an admin.
- **Create Exams:** Add new exams with titles, durations, and questions.
- **Manage Users:** View, promote, or delete student accounts.
- **Monitor Sessions:** Live view of ongoing exam sessions with face logs and alerts.

### Student Module

- **Register / Login:** Create a student account and log in.
- **Join Exams:** Enter exam code to start proctoring session.
- **Real-Time Monitoring:** Webcam feed is monitored, and tab switches are logged.
- **Submit Answers:** Complete questions before time expires.

---

## 📡 API Endpoints

| Method | Path                     | Description                        |
|--------|--------------------------|------------------------------------|
| POST   | `/login`                 | Authenticate and set user cookie   |
| GET    | `/admin/dashboard`       | Admin dashboard page               |
| GET    | `/admin/exams`           | List all exams                     |
| POST   | `/admin/exams`           | Create a new exam                  |
| GET    | `/admin/users`           | List all users                     |
| POST   | `/api/monitor/face_log`  | Record a face verification event   |
| POST   | `/api/monitor/tab_event` | Record a tab switch event          |
| _..._  | _expand this table with all your routes_ |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create a feature branch**  
     `git checkout -b feature/YourFeature`
3. **Commit your changes**  
     `git commit -m 'Add feature'`
4. **Push to the branch**  
     `git push origin feature/YourFeature`
5. **Open a Pull Request**

> Please ensure all new code is tested and documented.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

