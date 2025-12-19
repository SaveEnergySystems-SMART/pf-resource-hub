# 🔌 Backend API Endpoints Documentation
## User Management System for PF Resource Hub

---

## 🎯 Overview

This document outlines the **backend API endpoints** needed to connect the admin dashboards to a real database.

**Current Status**: Frontend uses **mock data**. These APIs need to be built in Flask backend.

---

## 🔐 Authentication

All admin endpoints require authentication via JWT token in the header:

```
Authorization: Bearer <JWT_TOKEN>
```

**Role-Based Access Control:**
- `ses_admin`: Full system access
- `pf_admin`: PF locations only
- `staff`: No admin access

---

## 📋 API Endpoints

### 1. **GET** `/api/admin/users`
**Get all users (with filtering)**

**Permissions**: `ses_admin`, `pf_admin`

**Query Parameters:**
- `location` (optional): Filter by PF location (e.g., `Boston Commons`)
- `role` (optional): Filter by role (`ses_admin`, `pf_admin`, `staff`, `manager`)
- `status` (optional): Filter by status (`active`, `inactive`)
- `search` (optional): Search by name or email

**Example Request:**
```bash
GET /api/admin/users?location=Boston Commons&status=active
Authorization: Bearer <TOKEN>
```

**Response (200 OK):**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john.smith@planetfitness.com",
      "role": "manager",
      "status": "active",
      "location": "Boston Commons",
      "created_at": "2024-01-15T10:30:00Z",
      "last_login": "2024-12-19T09:30:00Z"
    },
    {
      "id": 2,
      "name": "Sarah Johnson",
      "email": "sarah.j@planetfitness.com",
      "role": "staff",
      "status": "active",
      "location": "Boston Commons",
      "created_at": "2024-02-20T14:15:00Z",
      "last_login": "2024-12-19T08:15:00Z"
    }
  ],
  "total": 2
}
```

---

### 2. **POST** `/api/admin/users`
**Create new user**

**Permissions**: `ses_admin`, `pf_admin`

**Request Body:**
```json
{
  "name": "Emily Wilson",
  "email": "emily.w@planetfitness.com",
  "role": "staff",
  "location": "Cambridge"
}
```

**Backend Processing:**
1. Validate input data
2. Check if email already exists
3. **Generate random secure password** (e.g., `PF-xK9m2!vR4`)
4. Hash password with bcrypt
5. Create user in database
6. **Send welcome email** with:
   - Temporary password
   - Login link: `https://pf-resource-hub.pages.dev`
   - Instructions to change password on first login

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User created successfully. Welcome email sent.",
  "user": {
    "id": 15,
    "name": "Emily Wilson",
    "email": "emily.w@planetfitness.com",
    "role": "staff",
    "location": "Cambridge",
    "status": "active"
  },
  "email_sent": true
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Email already exists"
}
```

---

### 3. **PUT** `/api/admin/users/:id`
**Update user details**

**Permissions**: `ses_admin`, `pf_admin` (own location only)

**Request Body:**
```json
{
  "name": "Emily Wilson-Updated",
  "role": "manager",
  "location": "Cambridge"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User updated successfully",
  "user": {
    "id": 15,
    "name": "Emily Wilson-Updated",
    "email": "emily.w@planetfitness.com",
    "role": "manager",
    "location": "Cambridge",
    "status": "active"
  }
}
```

---

### 4. **POST** `/api/admin/users/:id/reset-password`
**Reset user password**

**Permissions**: `ses_admin`, `pf_admin` (own location only)

**Request Body:**
```json
{
  "send_email": true
}
```

**Backend Processing:**
1. Get user by ID
2. **Generate new random secure password** (e.g., `PF-aB7x!mN3`)
3. Hash password with bcrypt
4. Update password in database
5. Set `force_password_change` flag to `true`
6. **Send email** with:
   - New temporary password
   - Login link
   - Instructions to change password immediately

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successfully. Email sent.",
  "email_sent": true,
  "user_email": "emily.w@planetfitness.com"
}
```

---

### 5. **DELETE** `/api/admin/users/:id`
**Delete user (hard delete)**

**Permissions**: `ses_admin`, `pf_admin` (own location only)

**⚠️ WARNING**: This is a hard delete. User data will be permanently removed.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User deleted permanently",
  "deleted_user_id": 15
}
```

**Alternative: Soft Delete (Deactivate)**
Use `POST /api/admin/users/:id/deactivate` instead to preserve data.

---

### 6. **POST** `/api/admin/users/:id/deactivate`
**Deactivate user (soft delete)**

**Permissions**: `ses_admin`, `pf_admin` (own location only)

**Backend Processing:**
1. Set `status` to `inactive`
2. Revoke active sessions
3. Optionally send email notification

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User deactivated",
  "user": {
    "id": 15,
    "status": "inactive"
  }
}
```

---

### 7. **POST** `/api/admin/users/:id/activate`
**Activate user (restore access)**

**Permissions**: `ses_admin`, `pf_admin` (own location only)

**Backend Processing:**
1. Set `status` to `active`
2. Optionally send activation email

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User activated",
  "user": {
    "id": 15,
    "status": "active"
  }
}
```

---

### 8. **GET** `/api/admin/activity`
**Get activity log**

**Permissions**: `ses_admin`, `pf_admin`

**Query Parameters:**
- `location` (optional): Filter by location (for `pf_admin`)
- `limit` (optional): Number of results (default: 50)
- `offset` (optional): Pagination offset

**Response (200 OK):**
```json
{
  "success": true,
  "activities": [
    {
      "id": 1,
      "timestamp": "2024-12-19T09:45:00Z",
      "user_id": 1,
      "user_name": "John Smith",
      "action": "reset_password",
      "target_user": "Sarah Johnson",
      "location": "Boston Commons",
      "details": "Password reset for Sarah Johnson"
    },
    {
      "id": 2,
      "timestamp": "2024-12-19T09:30:00Z",
      "user_id": 4,
      "user_name": "Emily Wilson",
      "action": "login",
      "location": "Cambridge",
      "details": "User logged in"
    }
  ],
  "total": 156
}
```

---

### 9. **GET** `/api/admin/stats`
**Get dashboard statistics**

**Permissions**: `ses_admin`, `pf_admin`

**Query Parameters:**
- `location` (optional): Filter by location (for `pf_admin`)

**Response (200 OK):**
```json
{
  "success": true,
  "stats": {
    "total_users": 156,
    "active_users": 142,
    "inactive_users": 14,
    "total_locations": 6,
    "ses_admins": 12,
    "pf_admins": 6,
    "managers": 18,
    "staff": 120,
    "today_logins": 45,
    "today_activities": 23
  }
}
```

---

## 🔐 Password Generation

**Requirements for generated passwords:**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Example format: `PF-xK9m2!vR4`
- Stored as bcrypt hash in database

**Python Example:**
```python
import secrets
import string

def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return f"PF-{password[:4]}{secrets.choice('!@#$')}{password[4:8]}"
```

---

## 📧 Email Notifications

### Welcome Email (New User)
**Subject**: Welcome to PF Resource Hub

**Body:**
```
Hi [Name],

Your account has been created for the Planet Fitness & SES Resource Hub!

Login Information:
• Email: [email]
• Temporary Password: [password]
• Login URL: https://pf-resource-hub.pages.dev

⚠️ IMPORTANT: You will be required to change your password on first login.

Need help? Contact your administrator.

Best regards,
PF Resource Hub Team
```

### Password Reset Email
**Subject**: Your password has been reset

**Body:**
```
Hi [Name],

Your password has been reset by an administrator.

New Temporary Password: [password]
Login URL: https://pf-resource-hub.pages.dev

⚠️ Change your password immediately after logging in.

Best regards,
PF Resource Hub Team
```

---

## 🔨 Implementation Steps

### Phase 1: Database Schema (30 min)
1. Add `status` column to `users` table (`active`/`inactive`)
2. Add `location` column (e.g., `Boston Commons`, `Cambridge`)
3. Add `force_password_change` boolean column
4. Create `activity_log` table

### Phase 2: API Endpoints (2-3 hours)
1. Build GET /api/admin/users with filtering
2. Build POST /api/admin/users with password generation
3. Build PUT /api/admin/users/:id
4. Build POST /api/admin/users/:id/reset-password
5. Build DELETE /api/admin/users/:id
6. Build POST /api/admin/users/:id/deactivate
7. Build POST /api/admin/users/:id/activate
8. Build GET /api/admin/activity
9. Build GET /api/admin/stats

### Phase 3: Email Integration (1 hour)
1. Set up SendGrid API key
2. Create email templates
3. Test welcome emails
4. Test password reset emails

### Phase 4: Frontend Integration (1 hour)
1. Replace mock data with API calls
2. Add loading states
3. Add error handling
4. Test all CRUD operations

---

## 🧪 Testing Checklist

### User Creation:
- ✅ Create user with valid data
- ✅ Check password generated
- ✅ Check email sent
- ✅ Verify user can login with temp password
- ✅ Verify forced password change

### Password Reset:
- ✅ Reset password for existing user
- ✅ Check new password generated
- ✅ Check email sent
- ✅ Verify old password doesn't work
- ✅ Verify new password works

### User Update:
- ✅ Update user name
- ✅ Update user role
- ✅ Update user location
- ✅ Check changes persist

### User Delete/Deactivate:
- ✅ Deactivate user
- ✅ Verify user can't login
- ✅ Reactivate user
- ✅ Verify user can login again
- ✅ Hard delete user
- ✅ Verify user is gone

### Activity Log:
- ✅ Log user creation
- ✅ Log password reset
- ✅ Log user updates
- ✅ Log deactivations
- ✅ Log logins

---

## 💡 Next Steps

1. **Build these APIs in Flask backend**
2. **Connect admin dashboards to APIs**
3. **Set up SendGrid for emails**
4. **Test everything thoroughly**
5. **Deploy to production**

---

**Questions?** 
Let me know which endpoint you want to build first!
