# 🖥️ CUPCP Backend – Exam Registration API

This repository contains the **backend** for the CUPCP (Computer Club of Physics) Exam Registration system. It is built with **Django** and **Django REST Framework**, and uses **JWT** (via Simple JWT) for authentication.

---

## ⚙️ Technologies & Dependencies

- **Python 3.10+**  
- **Django 4.x**  
- **Django REST Framework**  
- **djangorestframework-simplejwt**  
- **SQLite** (default; easily switchable to PostgreSQL)  
- **django-cors-headers**  

---

## 📁 Project Structure

```text
CUPCProject/
├── accounts/
├── cupcp_backend/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── student_manager/
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
