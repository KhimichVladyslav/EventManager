# 🎉 Event Manager API

**Event Manager** is a REST API for managing events and user registrations.  
Built with **Django + Django REST Framework**, using **PostgreSQL**, **Docker**, and **JWT authentication**.

---

## 📂 Project Structure
```plaintext
event_manager/
├── events/         # Events and registrations app
├── users/          # User management app
├── event_manager/  # Project settings and main urls
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```
---

## ✅ **Features:**
- User registration & authentication (JWT tokens)
- CRUD for events
- Event registrations (unique per user + email notification)
- API documentation via **Swagger** and **ReDoc**
- Dockerized for easy setup
- Configurable via `.env` file


## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/KhimichVladyslav/EventManager.git
```

### 2. Environment variables

Create a `.env` file in the project root based on `.env.template`:

```env
# Django settings
DEBUG=1                     # 1 = dev mode, 0 = production
SECRET_KEY=your-secret-key  # Django secret key
DJANGO_ALLOWED_HOSTS='localhost 127.0.0.1 [::1] 0.0.0.0'

# Database settings
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=event_db
SQL_USER=event_user
SQL_PASSWORD=changeme
SQL_HOST=db
SQL_PORT=5432

# Superuser (auto-created at startup if not exists)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

# Email settings (for notifications (don't change it dude :) )
EMAIL_HOST_USER=event.manager.pro.lux@gmail.com
EMAIL_HOST_PASSWORD=pass   # e.g. Google App Password
```

---

### ⚙️ 3. Run with Docker (recommended)

```bash
docker compose up --build
```

This will:
1. Start a PostgreSQL container
2. Run Django inside a container
3. Apply migrations
4. Create a superuser (from `.env`)
5. Start the API on **http://localhost:8000**

---

### 4. Run locally (without Docker)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🔑 Authentication
- Uses **JWT (SimpleJWT)**.  
- Get token:
  ```
  POST /api/token/
  {
    "username": "admin",
    "password": "adminpass"
  }
  ```
- Use token in requests:
  ```
  Authorization: Bearer <your_access_token>
  ```

---

## 📚 API Documentation

Once the server is running:

- Swagger UI → [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)  
- ReDoc → [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)  

---

## 📌 API Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/events/` | GET, POST | List / Create events | JWT |
| `/api/events/{id}/` | GET, PUT, PATCH, DELETE | Event details | JWT (only organizer or admin can edit) |
| `/api/registrations/` | POST | Register for event | JWT |
| `/api/users/register/` | POST | Register a new user | Open |
| `/api/users/me/` | GET | Get current user info | JWT |
| `/api/token/` | POST | Obtain JWT token | Open |
| `/api/token/refresh/` | POST | Refresh JWT token | Open |
| `/api/docs/` | GET | Swagger UI | Open |

---

## 📩 Email Notifications

When a user registers firstly and registers for an event, they receive an email confirmation.  
Configure your SMTP credentials in `.env`:

- For Gmail → use an **App Password**  
- For development, you can set:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
This will print emails in the console instead of sending.

---

## 🧪 Running Tests

### Inside Docker (recommended)
1. Make sure your containers are running:
   ```bash
   docker compose up --build
   ```

2. Enter the web container:
   ```bash
   docker exec -it eventmanager-web-1 sh
   ```

3. Run the tests:
   ```bash
   pytest
   ```

## 🛡️ Permissions

- **Events:** Only the organizer (creator) or admin can edit/delete.  
- **Registrations:** Users can only register themselves.  
- **Users:**  
  - Registration → open  
  - Listing → only admins  
  - Delete → only admins

---

## 📦 Tech Stack

- Django 5
- Django REST Framework
- PostgreSQL
- SimpleJWT (auth)
- drf-yasg (API docs)
- Docker

---

👨‍💻 Author: **Vladyslav Khimich**  
📧 Contact: *khimich.vladyslav@gmail.com*
