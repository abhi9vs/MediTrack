# MediTrack# MediTrack
# MediTrack
MediTrack is a Hospital Management System built using Flask, SQLite, HTML, and CSS with role-based authentication for Admin, Doctor, and Patient. It supports appointment booking, doctor approval/rejection, patient management, and secure login.
# 🏥 MediTrack - Hospital Management System

MediTrack is a Hospital Management System built using **Python Flask**, **SQLite**, **HTML**, **CSS**, and **Flask Login Authentication**.

This project allows **Patients**, **Doctors**, and **Admins** to manage hospital appointments efficiently.

---

## 🚀 Features

### 👨‍⚕️ Doctor Panel
- Doctor Login
- View patient appointment requests
- Accept or Reject appointments
- Select appointment timing
- View approved appointments

### 🧑‍🤝‍🧑 Patient Panel
- Patient Login/Register
- Book appointments with doctors
- View appointment status
- Check approved/rejected appointments
- View doctor assigned timing

### 🛠️ Admin Panel
- Admin Login
- Add Patients
- View Patient List
- Delete Patients
- View all appointments

### 🔐 Authentication System
- Login using Email or Phone
- Password Hashing Security
- Role-based Authentication
- Secure Session Login

---

## 🧰 Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login

### Frontend
- HTML5
- CSS3

### Database
- SQLite

---

## 📂 Project Structure

```bash
MediTrack/
│── static/
│── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   ├── appointments.html
│   ├── doctor_appointments.html
│   ├── add_patient.html
│   ├── patients.html
│   └── book_appointment.html
│
│── instance/
│   └── database.db
│
│── app.py
│── README.md
│── requirements.txt
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/MediTrack.git
cd MediTrack
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### 3️⃣ Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run Project

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Login

Email:

```text
admin@meditrack.com
```

Password:

```text
admin123
```

---

## 📸 Screenshots

Add your project screenshots here.

Example:

- Home Page
- Login Page
- Doctor Dashboard
- Patient Dashboard
- Appointment Management

---

## 🔮 Future Improvements

- Doctor specialization
- Appointment search
- Email notifications
- Online payment integration
- Medical history records
- Prescription management

---

## 👨‍💻 Author

**Abhinav Shukla**

B.Tech CSE Student | Python & Web Development Enthusiast

---

## ⭐ Support

If you liked this project, give it a ⭐ on GitHub.

