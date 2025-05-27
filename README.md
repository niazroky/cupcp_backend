# cupcp_backend

A Django REST API backend that powers the **CUPCP** React frontend.

🔗 Visit the live app: [**cupcp.com**](https://cupcp.com)  
💻 Frontend source code: [**cupcp_frontend**](https://github.com/niazroky/cupcp_frontend)


This project exposes two main feature sets:

- **User Management** (students & teachers)

  - Registration & login (JWT)
  - Profile retrieval, update & logout

- **Exam Registration**
  - **Students**: create, view & update their own registrations
  - **Teachers**: view a summary of all exam registrations

---

## 🔧 Prerequisites

- **Python 3.9+**
- **pip** (package manager)
- **PostgreSQL** (or SQLite for quick local tests)
- **Node.js** & **npm** (for running the React frontend)

---

## 🔍 Highlights

- **GitHub CI/CD** workflow for automated testing & deployment  
- **Seamless API integration** with the React frontend  
- **Secure configuration** using a `.env` file for sensitive settings  
- **Robust PostgreSQL configuration** with environment-based settings for security and scalability
- **Fallback to SQLite** for local development  
- **Comprehensive documentation** and consistent code formatting  
- **Standardized HTTP responses** across all endpoints  


---

## Project Directory Tree

````plaintext
cupcp_backend/
├── .github/
│   └── workflows/
│       └── deploy_backend.yml
│
├── accounts/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_account_api.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── cupcp_backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── student_manager/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_exam_registration_api.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt

````
## ⚙️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/cupcp_backend.git
   cd cupcp_backend

   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   venv\Scripts\activate       # Windows

   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt

   ```

## 🔑 Environment Variables

Create a `.env` file alongside `manage.py` (see `.env.example`):

<pre><code class="language-dotenv">
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
ALLOWED_TEACHER_EMAILS=teacher1@domain.com,teacher2@domain.com
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
</code></pre>

**Security tip:**

- Never commit your real `.env` to version control.
- Set `DEBUG=False` in production.

---

## 🗄️ Database Setup

**Database URL for SQLite**
- For local development using SQLite, set the DATABASE_URL environment variable like this:
```bash
DATABASE_URL=sqlite:///db.sqlite3
```

**Generate migrations**

```bash
python manage.py makemigrations

```

**Apply migrations**

```bash
python manage.py migrate

```

**(Optional) Create a superuser**

```bash
python manage.py createsuperuser

```

## 🚀 Running Locally

**Start the Django development server:**

```bash
python manage.py runserver

```

**Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the API root.**

## 🛠️ API Endpoints

### 🔑 Authorization Header

Include the JWT **access token** in your request headers:

```http
Authorization: Bearer <access_token>

```

### 🔐 Authentication

| Method | URL                        | Description                           |
| ------ | -------------------------- | ------------------------------------- |
| POST   | `/auth/students/register/` | Student registration                  |
| POST   | `/auth/teachers/register/` | Teacher registration (whitelist only) |
| POST   | `/auth/students/login/`    | Student login (varsity ID + password) |
| POST   | `/auth/teachers/login/`    | Teacher login (email + password)      |
| POST   | `/auth/logout/`            | Blacklist refresh token (logout)      |
| POST   | `/auth/api/token/`         | Obtain JWT access & refresh tokens    |
| POST   | `/auth/api/token/refresh/` | Refresh access token                  |

### 🧾 Profile Management

| Method | URL           | Description                      |
| ------ | ------------- | -------------------------------- |
| GET    | `/auth/user/` | Retrieve authenticated user info |

### 📝 Exam Registration

| Method | URL                                           | Description                            |
| ------ | --------------------------------------------- | -------------------------------------- |
| GET    | `/student-manager/exam-registration/my/`      | Retrieve or check own registration     |
| POST   | `/student-manager/exam-registration/my/`      | Create a new registration              |
| PUT    | `/student-manager/exam-registration/my/`      | Update existing registration           |
| GET    | `/student-manager/exam-registration-summary/` | List all registrations (teachers only) |

## 🔗 Example Requests

1. **Student Registration**

   ```http
   POST /auth/students/register/
   Content-Type: application/json
   {
   "full_name": "Alice Smith",
   "email": "alice@student.com",
   "varsity_id": "12345678",
   "session": "2024-25",
   "gender": "female",
   "phone_number": "01122334455",
   "password": "abc123",
   "confirm_password": "abc123"
   }

   Response:

   "message": "Student registered successfully."
   ```

2. **Teacher Registration**

   ```http
   POST /auth/teachers/register/
   Content-Type: application/json

   {
   "full_name": "Dr. John Teacher",
   "email": "teacher@school.edu",
   "phone_number": "02233445566",
   "password": "teach12",
   "confirm_password": "teach12"
   }

   Response:

   "message": "Teacher registered successfully."

   ```

3. **Student Login**

   ```http
   POST /auth/students/login/
   Content-Type: application/json

   {
   "varsity_id": "12345678",
   "password": "abc123"
   }

   Response:
    {
        "access": "<jwt-access-token>",
        "refresh": "<jwt-refresh-token>",
        "role": "student"
    }

   ```

4. **Teacher Login**

   ```http
   POST /auth/teachers/login/
   Content-Type: application/json

   {
   "email": "teacher@school.edu",
   password": "teach12"
   }

   Response:
    {
        "access": "<jwt-access-token>",
        "refresh": "<jwt-refresh-token>",
        "role": "teacher"
    }

   ```

5. **Exam Registration**

   ```http
   POST /student-manager/exam-registration/my/
   Authorization: Bearer <access_token>
   Content-Type: application/json
   {
   "payment_status": "Yes",
   "payment_slip": "SLIP1001",
   "student_status": "regular",
   "courses": ["PHYS-401", "PHYS-402"],
   "hall_name": "Alaol Hall"
   }

   Response:
    {
        "registered": true,
        "registration": {
            /* registration object */
        }
    }

   ```

6. **Retrieve/Update Registration (Student Dashboard)**

   - **GET** `/student-manager/exam-registration/my/`  
     Retrieve the student's existing exam registration.

   - **PUT** `/student-manager/exam-registration/my/`  
     Update the registration using the same JSON payload (partial updates allowed).

7. **Exam Registration Summary (Teacher Dasboard)**

   ```
   GET /student-manager/exam-registration-summary/
   Authorization: Bearer <access_token>

   Response:
    [ /* Array of all exam registrations */ ]

   ```

### 📋 Admin Panel

Access `/admin/` with your superuser to manage users and registrations.

### 🧪 Running Tests

```bash
python manage.py test accounts
python manage.py test student_manager
```

Thanks for checking out this project!
Feel free to reach out via email at niazroky75@gmail.com if you'd like to connect or collaborate.
