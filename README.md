# 🩺 AI-Driven Blood Pressure Prediction System

A full-stack healthcare web application that predicts blood pressure levels using Machine Learning and provides intelligent health guidance through an interactive dashboard and chatbot.

---

## 📌 Project Overview

The **AI-Driven Blood Pressure Prediction System** is designed to help users analyze blood pressure risk levels based on patient health parameters such as:

* Age
* Height
* Weight
* Systolic BP
* Diastolic BP

The system predicts whether the patient falls under:

* ✅ Normal
* ⚠ Elevated
* 🚨 Hypertension

The project integrates:

* Machine Learning
* Flask Backend
* MySQL Database
* Interactive Dashboard
* Health Assistant Chatbot

---

# 🚀 Features

* 🔐 Secure Login & Signup
* 🤖 AI-Based BP Prediction
* 📊 Dashboard with Charts
* 💾 MySQL Database Storage
* 📋 Patient History Tracking
* 💬 Health Guidance Chatbot
* 🎨 Responsive UI Design
* ⚡ Real-Time Prediction

---

# 🛠 Technologies Used

## Frontend

* HTML
* CSS
* JavaScript
* Tailwind CSS
* Chart.js

## Backend

* Python
* Flask

## Database

* MySQL

## Machine Learning

* Scikit-learn
* StandardScaler
* Pickle

---

# 📂 Project Structure

```text
bp-project/
│
├── backend/
│   ├── app.py
│   ├── model.pkl
│   ├── scaler.pkl
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── style.css
│   └── script.js
│
├── dataset/
│   └── data.csv
│
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <your-github-repo-link>
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Virtual Environment

### Windows

```bash
.\venv\Scripts\activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 Database Setup

## Create Database

```sql
CREATE DATABASE bp_system;
```

## Create Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(255)
);
```

## Create Patients Table

```sql
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    height FLOAT,
    weight FLOAT,
    ap_hi FLOAT,
    ap_lo FLOAT,
    prediction VARCHAR(50)
);
```

---

# ▶️ Run Backend

```bash
cd backend
python app.py
```

Backend runs on:

```text
http://127.0.0.1:5000
```

---

# 🌐 Run Frontend

Open:

```text
index.html
```

or run using Flask templates.

---

# 📊 Workflow

```text
Login → Dashboard → Enter Patient Details
        ↓
Machine Learning Prediction
        ↓
Store in MySQL Database
        ↓
Display Table & Chart
        ↓
Chatbot Health Guidance
```

---

# 🤖 Chatbot Features

The chatbot provides:

* BP normal range
* Diet suggestions
* Exercise guidance
* Stress management tips
* Hypertension awareness
* Lifestyle recommendations

---


# 🎯 Future Enhancements

* ☁ Cloud Deployment
* 📱 Mobile Application
* 🤖 Real AI Chatbot API
* 🧠 Advanced Deep Learning Model
* 📄 PDF Report Generation
* 🩺 Doctor Dashboard
* 📡 IoT Device Integration

---

# 📚 References

* Flask Documentation
* Scikit-learn Documentation
* MySQL Documentation
* Chart.js Documentation
* Kaggle Healthcare Dataset

---

