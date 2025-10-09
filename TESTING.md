# 🧪 API Testing Guide

Complete guide to testing all 11 API endpoints.

## 🔧 Prerequisites

1. Server running: `python manage.py runserver`
2. Base URL: `http://localhost:8000/api/`
3. Admin user created: `walter45oyugi@gmail.com`

---

## 📋 Testing Checklist

- [ ] 1. POST `/api/auth/register/` - User registration
- [ ] 2. POST `/api/auth/verify-email/` - Email verification
- [ ] 3. POST `/api/auth/login/` - User login
- [ ] 4. GET `/api/auth/me/` - Get current user
- [ ] 5. POST `/api/auth/logout/` - Logout
- [ ] 6. POST `/api/auth/change-password/` - Change password
- [ ] 7. GET `/api/admin/users/` - Get all users
- [ ] 8. POST `/api/admin/create-user/` - Create user (admin)
- [ ] 9. GET `/api/auth/login-attempts/<email>/` - Login attempts
- [ ] 10. POST `/api/auth/request-admin-approval/` - Request approval
- [ ] 11. POST `/api/admin/approve-user/` - Admin approval

---

## 🧪 Test Cases

### 1️⃣ Register a New User

**Endpoint:** `POST /api/auth/register/`

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "password123",
    "role": "maintenance"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": 2,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": false,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login_at": null
  },
  "verification_code": "ABC123"
}
```

**Note:** Save the `verification_code` from the response.

---

### 2️⃣ Verify Email

**Endpoint:** `POST /api/auth/verify-email/`

```bash
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "ABC123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Email verified successfully! You can now log in."
}
```

---

### 3️⃣ Login

**Endpoint:** `POST /api/auth/login/`

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 2,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login_at": "2024-01-15T10:35:00Z"
  }
}
```

**Note:** Save the `token` from the response for authenticated requests.

---

### 4️⃣ Get Current User

**Endpoint:** `GET /api/auth/me/`

```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response:**
```json
{
  "success": true,
  "user": {
    "id": 2,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login_at": "2024-01-15T10:35:00Z"
  }
}
```

---

### 5️⃣ Change Password

**Endpoint:** `POST /api/auth/change-password/`

```bash
curl -X POST http://localhost:8000/api/auth/change-password/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "password123",
    "new_password": "newpassword456"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Password changed successfully!"
}
```

---

### 6️⃣ Logout

**Endpoint:** `POST /api/auth/logout/`

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 7️⃣ Get All Users (Admin Only)

**Endpoint:** `GET /api/admin/users/`

First, login as admin to get admin token:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "walter45oyugi@gmail.com",
    "password": "YOUR_ADMIN_PASSWORD"
  }'
```

Then use the admin token:

```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE"
```

**Expected Response:**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "email": "walter45oyugi@gmail.com",
      "first_name": "Walter",
      "last_name": "Oyugi",
      "role": "executive",
      "is_email_verified": true,
      "date_joined": "2024-01-01T00:00:00Z",
      "last_login_at": "2024-01-15T10:00:00Z"
    },
    {
      "id": 2,
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "maintenance",
      "is_email_verified": true,
      "date_joined": "2024-01-15T10:30:00Z",
      "last_login_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

---

### 8️⃣ Admin Create User

**Endpoint:** `POST /api/admin/create-user/`

```bash
curl -X POST http://localhost:8000/api/admin/create-user/ \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "password": "temppass123",
    "role": "executive"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "User created successfully!",
  "user": {
    "id": 3,
    "email": "jane.smith@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "executive",
    "is_email_verified": true,
    "date_joined": "2024-01-15T11:00:00Z",
    "last_login_at": null
  }
}
```

---

### 9️⃣ Get Login Attempts

**Endpoint:** `GET /api/auth/login-attempts/<email>/`

```bash
curl -X GET http://localhost:8000/api/auth/login-attempts/john.doe@example.com/
```

**Expected Response:**
```json
{
  "success": true,
  "email": "john.doe@example.com",
  "attempts": 0,
  "blocked": false,
  "admin_approved": false,
  "last_attempt": "2024-01-15T10:35:00Z"
}
```

---

### 🔟 Test Login Blocking

To test login attempt blocking:

1. **Try to login with wrong password 5 times:**

```bash
# Attempt 1
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "wrongpassword"
  }'
```

Response after 3rd attempt:
```json
{
  "success": false,
  "message": "Invalid credentials. 2 attempts remaining."
}
```

Response after 5th attempt:
```json
{
  "success": false,
  "message": "Account is blocked due to too many failed login attempts. Please contact admin for approval."
}
```

---

### 1️⃣1️⃣ Request Admin Approval

**Endpoint:** `POST /api/auth/request-admin-approval/`

```bash
curl -X POST http://localhost:8000/api/auth/request-admin-approval/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Admin approval request sent. Please wait for approval.",
  "admin_token": "admin_1706794800_abc123xyz"
}
```

**Note:** Save the `admin_token` for the next step.

---

### 1️⃣2️⃣ Admin Approve User

**Endpoint:** `POST /api/admin/approve-user/`

```bash
curl -X POST http://localhost:8000/api/admin/approve-user/ \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "admin_token": "admin_1706794800_abc123xyz"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "User approved successfully."
}
```

Now the user can login again!

---

## 🎯 Testing with Postman

### 1. Import Collection

Create a Postman collection with all endpoints.

### 2. Set Environment Variables

- `base_url`: `http://localhost:8000/api`
- `token`: (set after login)
- `admin_token`: (set after admin login)

### 3. Test All Endpoints

Use the collection to test each endpoint in order.

---

## 🔍 Testing Error Cases

### Invalid Email Format

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "role": "maintenance"
  }'
```

**Expected:** Validation error

### Password Too Short

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "123",
    "role": "maintenance"
  }'
```

**Expected:** "Password must be at least 6 characters long."

### Email Already Exists

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "role": "maintenance"
  }'
```

**Expected:** "User with this email already exists."

### Invalid Verification Code

```bash
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "code": "WRONG"
  }'
```

**Expected:** "Invalid verification code."

### Unauthorized Access to Admin Endpoint

```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer NON_ADMIN_TOKEN"
```

**Expected:** 403 Forbidden

---

## ✅ Test Results Template

Use this to track your testing:

```
✅ 1. POST /api/auth/register/ - PASSED
✅ 2. POST /api/auth/verify-email/ - PASSED
✅ 3. POST /api/auth/login/ - PASSED
✅ 4. GET /api/auth/me/ - PASSED
✅ 5. POST /api/auth/logout/ - PASSED
✅ 6. POST /api/auth/change-password/ - PASSED
✅ 7. GET /api/admin/users/ - PASSED
✅ 8. POST /api/admin/create-user/ - PASSED
✅ 9. GET /api/auth/login-attempts/<email>/ - PASSED
✅ 10. POST /api/auth/request-admin-approval/ - PASSED
✅ 11. POST /api/admin/approve-user/ - PASSED

All tests passed! ✨
```

---

**Happy Testing! 🚀**

