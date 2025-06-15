# 🧠 Face Monitor – Smart Exam Proctoring System

Face Monitor is an intelligent, web-based proctoring platform for secure, face-verified online exams. Built with **FastAPI**, **face-api.js**, and **HTML/CSS**, it verifies user identity in real-time and presents MCQ-based questions only if the registered face matches.

---

## 🚀 Features

- **Face Recognition Verification**  
    In-browser face verification using `face-api.js`
- **Student & Admin Dashboards**
- **MCQ-Based Question Rendering**
- **Real-time Webcam Feed**  
    Identity verification via webcam
- **Event Logging**  
    (e.g., unverified face, no face detected)
- **Secure Exam Access**  
    Questions load only after face verification

---

## 📁 Project Structure

```
project-root/
├── backend/        # FastAPI backend
├── frontend/       # HTML/CSS/JS (face-api.js)
├── database/       # DB files & models
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Register:**  
     Sign up with your name, email, student ID, and upload a clear photo.
2. **Login:**  
     Access your student dashboard.
3. **Start Exam:**  
     - Webcam opens for face verification.
     - On successful match, MCQ questions load.
     - Answer and submit your exam.
4. **Admin Access:**  
     - Log in via `/admin` to add/view questions.

---

## 📸 Face Verification Details

- Runs in-browser using `face-api.js` (TensorFlow.js)
- Compares live webcam feed with registered photo
- Verifies every **1.5 seconds**
- Reports events: _no face_, _wrong face_, etc.
- Blocks exam access if not verified

---

## 🔐 Security & Integrity

- 🧍‍♂️ **Only verified users** can access exams
- 👀 **Real-time monitoring** prevents impersonation
- 🛡️ **Proctoring logs** (DB storage coming soon)

---

## 🔧 Future Enhancements

- ⏲️ Countdown timer for each exam
- 📄 Save answers in database
- 📊 Result calculation & performance dashboard
- 📬 Email alerts on suspicious behavior

---

## 🙌 Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [face-api.js](https://github.com/justadudewhohacks/face-api.js)
- [Bootstrap](https://getbootstrap.com/) for UI
- **Your effort 👨‍💻 for putting this together!**

---

## 📜 License

[MIT License](LICENSE) – Free to use and modify.  
⭐ Star the repo if you find it useful!