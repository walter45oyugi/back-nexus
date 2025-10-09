# 🔐 Strathmore Insight Nexus - Authentication API

A Django REST API backend for secure user authentication with JWT tokens, email verification, and login attempt tracking.

## 🚀 Features

- ✅ User registration with email verification
- ✅ Secure login/logout with JWT tokens
- ✅ Password management (change password)
- ✅ Admin user management
- ✅ Role-based access control
- ✅ Login attempt tracking and blocking (max 5 attempts)
- ✅ Admin approval system for blocked users

## 📋 Requirements

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)

## 🛠️ Local Development Setup

### 1. Clone the repository

```bash
cd "back nexus"
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here-generate-a-random-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

Use these credentials:
- Email: `walter45oyugi@gmail.com`
- First name: `Walter`
- Last name: `Oyugi`
- Password: (choose a secure password)

After creation, open Django shell and set role:
```bash
python manage.py shell
```

Then in the shell:
```python
from api.models import User
user = User.objects.get(email='walter45oyugi@gmail.com')
user.role = 'executive'
user.is_email_verified = True
user.save()
exit()
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 🧪 Testing the API

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "role": "maintenance"
  }'
```

### Verify email

```bash
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "code": "ABC123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Get current user (with token)

```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## 📡 API Endpoints

### Authentication Endpoints

1. **POST** `/api/auth/register/` - User registration
2. **POST** `/api/auth/verify-email/` - Email verification
3. **POST** `/api/auth/login/` - User login (returns JWT token)
4. **GET** `/api/auth/me/` - Get current user info
5. **POST** `/api/auth/logout/` - Logout user
6. **POST** `/api/auth/change-password/` - Change password

### Admin Endpoints (requires admin token)

7. **GET** `/api/admin/users/` - Get all users
8. **POST** `/api/admin/create-user/` - Create user (pre-verified)
9. **POST** `/api/admin/approve-user/` - Approve blocked user

### Login Attempt Endpoints

10. **GET** `/api/auth/login-attempts/<email>/` - Get login attempts
11. **POST** `/api/auth/request-admin-approval/` - Request approval after block

## 🚀 Deployment on Render

### 1. Make build.sh executable

```bash
# On macOS/Linux
chmod +x build.sh

# On Windows (Git Bash)
git update-index --chmod=+x build.sh
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 3. Deploy on Render

1. Go to [Render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Click "Create Web Service"

### 4. Set environment variables on Render

Render will automatically set most variables from `render.yaml`, but verify:

- `SECRET_KEY` - Auto-generated
- `DATABASE_URL` - Auto-configured from PostgreSQL database
- `ALLOWED_HOSTS` - Set to `.onrender.com,localhost`
- `DEBUG` - Set to `False`

### 5. Create admin user on production

After deployment, go to Render dashboard → Shell tab:

```bash
python manage.py createsuperuser
```

Use:
- Email: `walter45oyugi@gmail.com`
- Password: (your secure password)

Then set role:
```bash
python manage.py shell
```

```python
from api.models import User
user = User.objects.get(email='walter45oyugi@gmail.com')
user.role = 'executive'
user.is_email_verified = True
user.save()
exit()
```

### 6. Get your production URL

Your API will be available at:
`https://your-app-name.onrender.com/api/`

## 🔐 Security Features

- **Password Hashing:** Django's built-in `make_password()`
- **JWT Tokens:** 5 hours for users, 1 year for admin
- **Login Attempt Tracking:** Max 5 attempts, then block
- **Email Verification:** Required before login
- **Role-Based Access:** Admin-only endpoints protected
- **CORS:** Configured for frontend domains

## 📝 Admin User

**Email:** `walter45oyugi@gmail.com`  
**Role:** Executive  
**Special Permissions:** Can access all admin endpoints

## 🔑 User Roles

- `maintenance` - Maintenance staff
- `cafeteria` - Cafeteria staff
- `security` - Security staff
- `executive` - Executive/Admin
- `iot-engineer` - IoT Engineer

## 📧 Email Configuration (Optional)

To enable email verification emails, update `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@strathmore.edu
```

For Gmail, you'll need to create an App Password:
1. Go to Google Account settings
2. Security → 2-Step Verification → App passwords
3. Generate a new app password
4. Use that password in `EMAIL_HOST_PASSWORD`

## 🆘 Troubleshooting

### Database migrations fail

```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### CORS errors

Make sure frontend URL is in `CORS_ALLOWED_ORIGINS` in `settings.py`

### JWT token errors

Make sure `SECRET_KEY` is set and consistent

### Import errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📚 Technology Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework** - API framework
- **Simple JWT** - JWT authentication
- **PostgreSQL** - Production database
- **Gunicorn** - WSGI server
- **Whitenoise** - Static file serving
- **CORS Headers** - Cross-origin requests

## 📄 License

This project is for educational purposes - Strathmore University.

## 👥 Contact

For issues or questions, contact: `walter45oyugi@gmail.com`

---

**Made with ❤️ for Strathmore Insight Nexus**

