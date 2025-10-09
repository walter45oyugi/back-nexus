# 🔧 Environment Variable Setup Guide

## Development Environment (.env)

Create a `.env` file in the root directory with the following variables:

```env
# =============================================================================
# DJANGO SETTINGS
# =============================================================================

# Secret key for Django (generate a new one for production)
# Generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=django-insecure-change-this-in-production-abc123xyz789

# Debug mode (set to False in production)
DEBUG=True

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# =============================================================================
# DATABASE
# =============================================================================

# Database URL (leave empty to use SQLite in development)
# For PostgreSQL: postgresql://user:password@host:port/database
DATABASE_URL=

# =============================================================================
# EMAIL SETTINGS (Optional - for email verification)
# =============================================================================

# Email backend
# Development: django.core.mail.backends.console.EmailBackend (prints to console)
# Production: django.core.mail.backends.smtp.EmailBackend
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# SMTP settings (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Your email credentials
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Default from email
DEFAULT_FROM_EMAIL=noreply@strathmore.edu
```

---

## Production Environment (Render.com)

Set these environment variables in your Render.com dashboard:

### Required Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Auto-generated | Let Render generate this |
| `DEBUG` | `False` | Never set to True in production |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` | Your production domain |
| `DATABASE_URL` | Auto-configured | Render sets this from PostgreSQL |

### Optional Variables (Email)

| Variable | Value | Notes |
|----------|-------|-------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | For sending real emails |
| `EMAIL_HOST` | `smtp.gmail.com` | Your SMTP host |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USE_TLS` | `True` | Use TLS |
| `EMAIL_HOST_USER` | `your-email@gmail.com` | Your email |
| `EMAIL_HOST_PASSWORD` | `your-app-password` | Gmail app password |
| `DEFAULT_FROM_EMAIL` | `noreply@strathmore.edu` | From email address |

---

## 🔑 Generating a Secret Key

### Method 1: Using Django

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Method 2: Using Python

```python
import secrets
print(secrets.token_urlsafe(50))
```

### Method 3: Online Generator

Visit: https://djecrety.ir/

---

## 📧 Setting Up Gmail for Email

If you want to send verification emails using Gmail:

### 1. Enable 2-Step Verification

1. Go to your Google Account settings
2. Security → 2-Step Verification
3. Turn it on

### 2. Create App Password

1. Go to Google Account → Security
2. 2-Step Verification → App passwords
3. Select "Mail" and "Other (Custom name)"
4. Name it "Strathmore Auth API"
5. Click "Generate"
6. Copy the 16-character password
7. Use this in `EMAIL_HOST_PASSWORD`

### 3. Update .env

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=the-16-char-app-password
DEFAULT_FROM_EMAIL=noreply@strathmore.edu
```

---

## 🗄️ Database Configuration

### Development (SQLite)

Leave `DATABASE_URL` empty in `.env`:

```env
DATABASE_URL=
```

Django will automatically use SQLite (`db.sqlite3`).

### Production (PostgreSQL on Render)

Render automatically sets `DATABASE_URL` when you create a PostgreSQL database.

Format:
```
postgresql://user:password@host:port/database
```

### Local PostgreSQL (Optional)

If you want to use PostgreSQL locally:

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE strathmore_db;
CREATE USER strathmore_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE strathmore_db TO strathmore_user;
```

3. Set in `.env`:
```env
DATABASE_URL=postgresql://strathmore_user:your_password@localhost:5432/strathmore_db
```

---

## ✅ Environment Variable Checklist

### Development

- [ ] `SECRET_KEY` set (any random string is fine)
- [ ] `DEBUG=True`
- [ ] `ALLOWED_HOSTS` includes localhost
- [ ] `DATABASE_URL` empty (uses SQLite)
- [ ] `EMAIL_BACKEND` set to console backend

### Production

- [ ] `SECRET_KEY` generated and secure
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` includes production domain
- [ ] `DATABASE_URL` configured (PostgreSQL)
- [ ] Email settings configured (optional)

---

## 🔍 Testing Environment Variables

Create a test script `test_env.py`:

```python
import os
from decouple import config

print("Testing environment variables...")
print(f"SECRET_KEY: {'✅ Set' if config('SECRET_KEY', default=None) else '❌ Not set'}")
print(f"DEBUG: {config('DEBUG', default=True, cast=bool)}")
print(f"ALLOWED_HOSTS: {config('ALLOWED_HOSTS', default='localhost')}")
print(f"DATABASE_URL: {'✅ Set' if config('DATABASE_URL', default=None) else '❌ Not set (using SQLite)'}")
print(f"EMAIL_BACKEND: {config('EMAIL_BACKEND', default='console')}")
```

Run it:
```bash
python test_env.py
```

---

## 🆘 Troubleshooting

### "SECRET_KEY not found"

Create a `.env` file in the root directory with `SECRET_KEY=your-key-here`

### "Database connection failed"

Check `DATABASE_URL` format and credentials

### "Email not sending"

1. Check `EMAIL_BACKEND` is set to SMTP backend
2. Verify Gmail app password is correct
3. Check Gmail 2-Step Verification is enabled

### "ALLOWED_HOSTS error"

Add your domain to `ALLOWED_HOSTS` in `.env`:
```env
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com,your-domain.com
```

---

**Need help?** Contact: `walter45oyugi@gmail.com`

