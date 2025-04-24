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
cupcp_backend/
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
```

---

## 🚀 How to Run the Project Locally

Follow these steps to set up and run the Django backend on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cupcp_backend.git
cd cupcp_backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your secret keys and settings:

```ini
SECRET_KEY=your-secret-key
DEBUG=True
And there are more...
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional, for Admin Panel)

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

---

The backend will be running at `http://127.0.0.1:8000/` by default.

Let me know if you'd like to also document API endpoints, authentication flow, or setup for production deployment.
