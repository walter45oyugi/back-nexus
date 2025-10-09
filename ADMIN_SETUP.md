# 👨‍💼 Admin User Setup Guide

## ⚠️ Important: Creating Admin User on Render Free Tier

Since you're on Render's free tier and can't access the shell, here are your options:

---

## Option 1: Use Django Admin Panel (RECOMMENDED ✅)

### Step 1: Access Django Admin
Go to: `https://back-nexus.onrender.com/admin/`

### Step 2: Create Superuser via Script
We'll create a special endpoint just for first-time admin creation.

**I'll add this endpoint for you - it will be a one-time setup endpoint.**

---

## Option 2: Register Normally + Manual Database Update

### Step 1: Register via API
Use the regular registration endpoint:

```bash
curl -X POST https://back-nexus.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "walter45oyugi@gmail.com",
    "first_name": "Walter",
    "last_name": "Oyugi",
    "password": "YOUR_SECURE_PASSWORD",
    "role": "executive"
  }'
```

### Step 2: Verify Email
```bash
curl -X POST https://back-nexus.onrender.com/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "walter45oyugi@gmail.com",
    "code": "THE_CODE_FROM_REGISTRATION_RESPONSE"
  }'
```

### Step 3: Contact Render Support
Since you have a PostgreSQL database, you can:
1. Go to your PostgreSQL database in Render
2. Click "Access" tab
3. Use the provided connection details to connect via a PostgreSQL client
4. Run this SQL:

```sql
UPDATE api_user 
SET is_staff = true, is_superuser = true, role = 'executive' 
WHERE email = 'walter45oyugi@gmail.com';
```

---

## Option 3: One-Time Setup Endpoint (BEST FOR FREE TIER)

I'll create a special endpoint that only works once to create the admin user.

**Endpoint:** `POST /api/admin/setup/`

**Request:**
```json
{
  "email": "walter45oyugi@gmail.com",
  "password": "YOUR_SECURE_PASSWORD",
  "first_name": "Walter",
  "last_name": "Oyugi",
  "setup_key": "STRATHMORE2024NEXUS"
}
```

**This endpoint:**
- Only works if NO admin exists yet
- Requires a secret setup key
- Creates admin with all permissions
- Automatically disables itself after first use

---

## 📝 What You Need to Do Now

**Choose Option 3 (I'll implement it now)** - it's the easiest for your situation!

After the endpoint is created, you'll just make ONE API call to create your admin user, then you're done!

---

## ✅ After Admin User is Created

You can then:
1. Login at `https://back-nexus.onrender.com/api/auth/login/`
2. Access all admin endpoints
3. Create more users via `/api/admin/create-user/`
4. Approve blocked users
5. View all members

---

**Let me implement Option 3 for you now!**

