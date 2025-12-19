# Planet Fitness Resource Hub - Backend API

## 🚀 Quick Start

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update environment variables
3. Get SendGrid API key from https://sendgrid.com

### Run Locally
```bash
python app.py
```

API will run on `http://localhost:5000`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/forgot-username` - Request username reminder
- `POST /api/auth/reset-password` - Reset password with token
- `POST /api/auth/change-password` - Change password (authenticated)

### User Management (Admin Only)
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `PUT /api/users/<username>` - Update user
- `DELETE /api/users/<username>` - Delete user (SES admin only)
- `POST /api/users/<username>/reset-password` - Admin reset user password

### Health
- `GET /api/health` - Health check
- `GET /` - API info

## 🔐 Default Admin Accounts

**SES Super Admin:**
- Username: `ses_admin`
- Password: `Admin123!` (CHANGE THIS!)
- Email: admin@saveenergysystems.com

**PF Admin:**
- Username: `pf_admin`
- Password: `PFAdmin123!` (CHANGE THIS!)
- Email: manager@planetfitness.com

## 🛠️ Tech Stack
- Python 3.11+
- Flask (web framework)
- Flask-CORS (CORS handling)
- PyJWT (JWT authentication)
- SendGrid (email service)
- PostgreSQL (database)

## 🚢 Deployment

### Railway
1. Connect GitHub repo
2. Select `backend` directory
3. Add environment variables
4. Deploy!

### Environment Variables Required
- `SECRET_KEY`
- `SENDGRID_API_KEY`
- `FRONTEND_URL`
- `DATABASE_URL` (auto-provided by Railway)
