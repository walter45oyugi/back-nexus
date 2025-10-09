# ⚡ Quick Start Guide

Get the backend running in 5 minutes!

## 🚀 Steps

### 1️⃣ Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Setup Environment

Create a `.env` file:

```env
SECRET_KEY=django-insecure-dev-key-for-local-testing-only
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
```

### 3️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Create Admin User

```bash
python create_admin.py
```

Follow the prompts:
- Email: `walter45oyugi@gmail.com` (default)
- Password: Choose a secure password
- First name: Walter
- Last name: Oyugi

### 5️⃣ Start Server

```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

### 6️⃣ Test API

Open a new terminal and test:

```bash
# Register a user
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

---

## ✅ Success!

Your API is now running! 🎉

### Next Steps:

1. **Read full documentation:** `README.md`
2. **Test all endpoints:** `TESTING.md`
3. **Deploy to production:** Follow deployment section in `README.md`

---

## 🆘 Having Issues?

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "No such table"
```bash
python manage.py migrate
```

### "ALLOWED_HOSTS error"
Make sure `.env` file exists with `ALLOWED_HOSTS=localhost,127.0.0.1`

---

## 📚 Documentation Files

- `README.md` - Complete documentation
- `TESTING.md` - Testing guide with all endpoints
- `ENV_SETUP.md` - Environment variable configuration
- `BACKEND_HANDOVER.md` - Handover template for frontend team
- `QUICKSTART.md` - This file

---

**Need help?** Check `README.md` or contact: `walter45oyugi@gmail.com`

