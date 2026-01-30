# 🎬 Movie Ticket Booking System (Django)

## 📌 Project Description
A **Django-based Movie Ticket Booking System** that allows users to browse movies, view details, and book tickets online. This project demonstrates real-world full-stack development using Django, templates, static files, and database integration.

---

## 🎥 Project Overview
The **Movie Ticket Booking System** is a web application developed using **Django**.  
It simulates an online cinema booking platform where movies, posters, and booking-related data are managed efficiently. The Django Admin Panel is used for backend management.

This project is developed as part of **Python Full Stack Development** learning and is suitable for **fresher-level job applications**.

---

## 🚀 Features
- Movie listing and detail pages  
- Movie poster upload and display  
- Ticket booking workflow  
- Django Admin Panel for managing data  
- Form handling using Django Forms  
- Static files (CSS & JavaScript)  
- Media file handling  
- SQLite database integration  

---

## 🛠️ Tech Stack
**Backend**
- Python 3  
- Django  

**Frontend**
- HTML5  
- CSS3  
- JavaScript  
- Bootstrap  

**Database**
- SQLite3  

---

## 🗂️ Project Structure
movietix/
│
├── cinema/
│ ├── pycache/
│ ├── migrations/
│ ├── templates/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
│
├── media/
│
├── movietix/
│ ├── pycache/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── static/
│ └── cinema/
│ ├── css/
│ └── js/
│
├── staticfiles/
│ ├── admin/
│ └── cinema/
│
├── venv/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

---


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Dhanalakshmi-thumu/Movie-Ticket-Booking-System.git
cd Movie-Ticket-Booking-System

2️⃣ Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Admin User
python manage.py createsuperuser

6️⃣ Run the Server
python manage.py runserver


Open in browser:

http://127.0.0.1:8000/


Admin Panel:

http://127.0.0.1:8000/admin/

🎯 Learning Outcomes

Understanding Django MVT architecture

Working with models, views, and templates

Handling static and media files

CRUD operations using Django ORM

Admin panel usage

🔮 Future Enhancements

User authentication and authorization

Seat selection system

Online payment gateway integration

Booking history

Email confirmation for bookings

👩‍💻 Author

Dhanalaksmi Thumu
Aspiring Python Full Stack Developer (Fresher)

📜 License

This project is created for learning and educational purposes only.


---

## ✅ After pasting (FINAL STEP)
Run these commands in VS Code terminal:

```bash
git add README.md
git commit -m "Added project README"
git push -u origin main

