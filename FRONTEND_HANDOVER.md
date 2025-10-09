# 📤 Backend Handover - Strathmore Insight Nexus

## ✅ Deployment Information

**Production API Base URL:**  
```
https://back-nexus.onrender.com/api/
```

**Admin Email:** `walter45oyugi@gmail.com`  
**Admin Password:** `[SET YOUR PASSWORD WHEN CREATING ADMIN USER]`

---

## 🔐 Authentication Flow

### Session Timeout: **20 Minutes**
- User tokens expire after 20 minutes of inactivity
- Admin tokens expire after 1 year
- Frontend should redirect to login on 401 errors

---

## 📡 Available API Endpoints

### 1️⃣ User Registration
**POST** `/api/auth/register/`

**Request:**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securePassword123",
  "role": "maintenance"
}
```

**Roles:** `maintenance`, `cafeteria`, `security`, `executive`, `iot-engineer`

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": false
  },
  "verification_code": "ABC123"
}
```

---

### 2️⃣ Email Verification
**POST** `/api/auth/verify-email/`

**Request:**
```json
{
  "email": "user@example.com",
  "code": "ABC123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Email verified successfully! You can now log in."
}
```

---

### 3️⃣ User Login
**POST** `/api/auth/login/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": true,
    "last_login_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error - Account Blocked (403):**
```json
{
  "success": false,
  "message": "Account is blocked due to too many failed login attempts. Please contact admin for approval."
}
```

**Frontend Action:** Store the `token` in localStorage and use it for all authenticated requests.

---

### 4️⃣ Get Current User
**GET** `/api/auth/me/`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "maintenance",
    "is_email_verified": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login_at": "2024-01-15T10:30:00Z"
  }
}
```

**Use this to:** Check if user is still authenticated, get user info for dashboard.

---

### 5️⃣ Change Password
**POST** `/api/auth/change-password/`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request:**
```json
{
  "current_password": "oldPassword123",
  "new_password": "newPassword456"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password changed successfully!"
}
```

---

### 6️⃣ Logout
**POST** `/api/auth/logout/`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Frontend Action:** Clear token from localStorage and redirect to login.

---

## 👨‍💼 Admin Endpoints

### 7️⃣ Get All Users (Admin Only)
**GET** `/api/admin/users/`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Response (200):**
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
      "email": "user@example.com",
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

**Use for:** Admin dashboard to show all registered members.

---

### 8️⃣ Create User (Admin Only)
**POST** `/api/admin/create-user/`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request:**
```json
{
  "email": "newuser@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "password": "tempPassword123",
  "role": "executive"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User created successfully!",
  "user": {
    "id": 3,
    "email": "newuser@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "executive",
    "is_email_verified": true
  }
}
```

**Note:** Admin-created users are pre-verified (no email verification needed).

---

### 9️⃣ Get Login Attempts
**GET** `/api/auth/login-attempts/<email>/`

**Example:** `/api/auth/login-attempts/user@example.com/`

**Response (200):**
```json
{
  "success": true,
  "email": "user@example.com",
  "attempts": 2,
  "blocked": false,
  "admin_approved": false,
  "last_attempt": "2024-01-15T10:30:00Z"
}
```

**Use for:** Show user their remaining login attempts.

---

### 🔟 Request Admin Approval
**POST** `/api/auth/request-admin-approval/`

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Admin approval request sent. Please wait for approval.",
  "admin_token": "admin_1706794800_abc123"
}
```

**Use when:** User is blocked after 5 failed login attempts.

---

### 1️⃣1️⃣ Admin Approve Blocked User
**POST** `/api/admin/approve-user/`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request:**
```json
{
  "email": "user@example.com",
  "admin_token": "admin_1706794800_abc123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "User approved successfully."
}
```

---

## 🔒 Frontend Implementation Guide

### 1. Login Flow
```javascript
// Login function
async function login(email, password) {
  const response = await fetch('https://back-nexus.onrender.com/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Store token
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    // Set token expiry (20 minutes from now)
    const expiryTime = Date.now() + (20 * 60 * 1000);
    localStorage.setItem('tokenExpiry', expiryTime);
    
    // Redirect to dashboard
    window.location.href = '/dashboard';
  } else {
    alert(data.message);
  }
}
```

### 2. Session Timeout (20 Minutes)
```javascript
// Check if token is expired
function isTokenExpired() {
  const expiryTime = localStorage.getItem('tokenExpiry');
  if (!expiryTime) return true;
  
  return Date.now() > parseInt(expiryTime);
}

// Middleware for protected routes
function checkAuth() {
  const token = localStorage.getItem('token');
  
  if (!token || isTokenExpired()) {
    // Clear storage
    localStorage.clear();
    // Redirect to login
    window.location.href = '/login';
    return false;
  }
  
  return true;
}

// Update expiry on user activity
function updateTokenExpiry() {
  const expiryTime = Date.now() + (20 * 60 * 1000);
  localStorage.setItem('tokenExpiry', expiryTime);
}

// Add event listeners for user activity
['click', 'keypress', 'scroll', 'mousemove'].forEach(event => {
  document.addEventListener(event, updateTokenExpiry);
});
```

### 3. API Request Helper
```javascript
async function apiRequest(endpoint, method = 'GET', body = null) {
  // Check auth before request
  if (!checkAuth()) return;
  
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
  
  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);
  
  const response = await fetch(`https://back-nexus.onrender.com/api${endpoint}`, options);
  const data = await response.json();
  
  // Handle 401 (unauthorized - token expired)
  if (response.status === 401) {
    localStorage.clear();
    window.location.href = '/login';
    return null;
  }
  
  return data;
}

// Example usage
async function getCurrentUser() {
  return await apiRequest('/auth/me/');
}

async function getAllUsers() {
  return await apiRequest('/admin/users/');
}
```

### 4. Registration Flow
```javascript
async function register(formData) {
  const response = await fetch('https://back-nexus.onrender.com/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Show verification code (in development)
    alert(`Registration successful! Verification code: ${data.verification_code}`);
    // Redirect to verification page
    window.location.href = `/verify-email?email=${formData.email}`;
  } else {
    alert(data.message);
  }
}
```

### 5. Admin Dashboard - Show All Members
```javascript
async function loadMembers() {
  const data = await apiRequest('/admin/users/');
  
  if (data && data.success) {
    const members = data.users;
    
    // Display in table
    const tableBody = document.getElementById('membersTable');
    tableBody.innerHTML = members.map(user => `
      <tr>
        <td>${user.email}</td>
        <td>${user.first_name} ${user.last_name}</td>
        <td>${user.role}</td>
        <td>${user.is_email_verified ? 'Yes' : 'No'}</td>
        <td>${new Date(user.last_login_at).toLocaleString()}</td>
      </tr>
    `).join('');
  }
}
```

---

## 🎨 UI/UX Recommendations

### Login Screen
- Email input
- Password input (with show/hide toggle)
- "Remember me" checkbox (optional)
- Login button
- "Forgot password?" link
- "Register" link
- Show remaining attempts after failed login

### Registration Screen
- Email
- First Name
- Last Name
- Password
- Confirm Password
- Role (dropdown)
- Register button

### Admin Dashboard
**Sections:**
1. **Total Members** - Count of all registered users
2. **Recent Logins** - Show users with `last_login_at` sorted by date
3. **Members Table** - All users with:
   - Email
   - Name
   - Role
   - Verified status
   - Last login time
4. **Blocked Users** - Users who need approval

---

## ⚠️ Error Handling

```javascript
// Handle different error scenarios
async function handleApiError(response, data) {
  if (response.status === 401) {
    // Unauthorized - token expired
    localStorage.clear();
    window.location.href = '/login';
  } else if (response.status === 403) {
    // Forbidden - account blocked or not admin
    alert(data.message);
  } else if (response.status === 400) {
    // Bad request - validation error
    alert(data.message);
  } else {
    // Generic error
    alert('An error occurred. Please try again.');
  }
}
```

---

## 🔑 Important Notes for Frontend

1. **Token Storage:** Store JWT token in `localStorage` or `sessionStorage`
2. **Token Expiry:** Implement 20-minute timeout with auto-logout
3. **Authorization Header:** Always send `Authorization: Bearer TOKEN` for protected routes
4. **CORS:** Already configured for `http://localhost:5173` and your production domain
5. **Error Handling:** Check for `success: false` in responses
6. **Admin Check:** Only `walter45oyugi@gmail.com` can access admin endpoints
7. **Login Attempts:** Show warning after 3 failed attempts, block after 5

---

## 🧪 Testing the API

**Test Login:**
```bash
curl -X POST https://back-nexus.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "walter45oyugi@gmail.com",
    "password": "YOUR_ADMIN_PASSWORD"
  }'
```

**Test Get Current User:**
```bash
curl -X GET https://back-nexus.onrender.com/api/auth/me/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📞 Support

**Backend Developer:** Walter Oyugi  
**Email:** walter45oyugi@gmail.com  
**API Base URL:** https://back-nexus.onrender.com/api/

---

## ✅ Checklist for Frontend Team

- [ ] Implement login page
- [ ] Implement registration page
- [ ] Implement email verification page
- [ ] Add JWT token management
- [ ] Add 20-minute session timeout
- [ ] Create admin dashboard
- [ ] Show all registered members
- [ ] Handle token expiry (401 errors)
- [ ] Show login attempt warnings
- [ ] Test all API endpoints

---

**🎉 Your backend is ready! Happy coding!**

