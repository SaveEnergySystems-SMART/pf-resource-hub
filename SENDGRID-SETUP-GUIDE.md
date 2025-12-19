# 📧 SendGrid Email Setup Guide
## For PF Resource Hub Password Resets & Username Recovery

---

## 🎯 What We're Setting Up

**Email Types:**
1. **Password Reset** - User forgot password
2. **Username Recovery** - User forgot username/email
3. **Welcome Email** - New user created by admin
4. **Admin Password Reset** - Admin resets user's password

---

## 📋 STEP 1: Create SendGrid Account

### 1. Go to SendGrid:
🔗 **https://signup.sendgrid.com/**

### 2. Sign Up (FREE tier is perfect for you):
- **Free Plan**: 100 emails/day forever
- More than enough for password resets

### 3. Fill out the form:
- Email: Your email
- Password: Strong password
- Complete verification

### 4. Verify your email address
- Check your inbox
- Click verification link

---

## 📋 STEP 2: Get Your API Key

### 1. Login to SendGrid Dashboard:
🔗 **https://app.sendgrid.com/**

### 2. Navigate to API Keys:
- Left sidebar → **Settings** → **API Keys**
- Or direct link: https://app.sendgrid.com/settings/api_keys

### 3. Click **"Create API Key"**

### 4. Configure the API Key:
- **API Key Name**: `PF-Resource-Hub-Production`
- **API Key Permissions**: Select **"Restricted Access"**
  - Expand **Mail Send** → Toggle ON **"Mail Send"**
  - Expand **Template Engine** → Toggle ON **"Read"** and **"Create"**
  - Leave everything else OFF

### 5. Click **"Create & View"**

### 6. **COPY THE API KEY** (looks like this):
```
SG.xxxxxxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

⚠️ **IMPORTANT**: Save this key! You can only see it once!

---

## 📋 STEP 3: Verify Sender Email

SendGrid requires you to verify the email address you'll send FROM.

### 1. Navigate to Sender Authentication:
- Left sidebar → **Settings** → **Sender Authentication**
- Or: https://app.sendgrid.com/settings/sender_auth

### 2. Choose **"Single Sender Verification"** (easiest):
- Click **"Verify a Single Sender"**

### 3. Fill out the form:
```
From Name: PF Resource Hub
From Email Address: noreply@saveenergysystems.com
Reply To: support@saveenergysystems.com (or your real support email)
Company Address: (your address)
City: Boston
State: MA
Zip: 02108
Country: United States
```

### 4. Click **"Create"**

### 5. Check your email (noreply@saveenergysystems.com):
- You'll receive a verification email
- Click the verification link

### 6. ✅ Once verified, you can send emails from this address!

---

## 📋 STEP 4: Add API Key to Backend

### 1. Open your backend `.env` file:
```bash
cd /home/user/pf-resource-hub/backend
nano .env
```

### 2. Add SendGrid configuration:
```bash
# SendGrid Configuration
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
SENDGRID_FROM_EMAIL=noreply@saveenergysystems.com
SENDGRID_FROM_NAME=PF Resource Hub

# Frontend URL (for email links)
FRONTEND_URL=https://pf-resource-hub.pages.dev
# For local testing: http://localhost:3000
```

### 3. Save and exit:
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter`

---

## 📋 STEP 5: Install SendGrid in Backend

### 1. Install the SendGrid Python library:
```bash
cd /home/user/pf-resource-hub/backend
pip install sendgrid
```

### 2. Verify installation:
```bash
pip list | grep sendgrid
```

Should show:
```
sendgrid    6.11.0
```

---

## 📋 STEP 6: Create Email Service File

I'll create this for you with all the email templates!

### File: `backend/email_service.py`

This will include:
- Password reset email
- Username recovery email
- Welcome email for new users
- Admin password reset notification

---

## 📋 STEP 7: Create Email Templates

### Option A: Use Simple Text Emails (EASIEST - I'll build this)
- Plain text emails
- No design needed
- Works immediately

### Option B: Use HTML Templates (FANCY - Optional)
- Professional-looking emails
- Brand colors (purple/yellow)
- Takes more time

**Recommendation**: Start with Option A (simple text), upgrade to HTML later.

---

## 🔧 WHAT I'LL BUILD FOR YOU

### 1. **Email Service** (`backend/email_service.py`):
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

class EmailService:
    def send_password_reset(self, to_email, reset_token):
        # Send password reset email with link
        
    def send_username_recovery(self, to_email, username):
        # Send forgotten username
        
    def send_welcome_email(self, to_email, temp_password):
        # Send welcome email with temp password
        
    def send_admin_password_reset(self, to_email, new_temp_password):
        # Send admin-triggered password reset
```

### 2. **Backend API Endpoints**:
```python
POST /api/auth/forgot-password
  → Sends reset link to email

POST /api/auth/forgot-username
  → Sends username to email

POST /api/auth/reset-password/:token
  → Resets password with token

POST /api/admin/users/:id/reset-password
  → Admin resets user password + sends email
```

### 3. **Frontend Pages**:
- Forgot Password page
- Forgot Username page
- Reset Password page (with token)

---

## 📧 EMAIL TEMPLATES (SIMPLE TEXT)

### 1. Password Reset Email:
```
Subject: Reset Your PF Resource Hub Password

Hi,

You requested to reset your password for the PF Resource Hub.

Click this link to reset your password:
https://pf-resource-hub.pages.dev/reset-password?token=abc123

This link expires in 1 hour.

If you didn't request this, ignore this email.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
```

### 2. Username Recovery Email:
```
Subject: Your PF Resource Hub Username

Hi,

You requested your username for the PF Resource Hub.

Your username/email is: john.smith@planetfitness.com

Login here: https://pf-resource-hub.pages.dev

---
PF Resource Hub Team
Support: support@saveenergysystems.com
```

### 3. Welcome Email (New User):
```
Subject: Welcome to PF Resource Hub

Hi John Smith,

Your account has been created for the PF Resource Hub!

Login Information:
Email: john.smith@planetfitness.com
Temporary Password: PF-xK9m!vR4

Login here: https://pf-resource-hub.pages.dev

⚠️ You must change your password on first login.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
```

### 4. Admin Password Reset:
```
Subject: Your Password Has Been Reset

Hi John Smith,

Your password has been reset by an administrator.

New Temporary Password: PF-aB7x!mN3

Login here: https://pf-resource-hub.pages.dev

⚠️ Change your password immediately after logging in.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
```

---

## 🧪 TESTING EMAILS

### 1. Test with your own email first:
```bash
# In backend directory
python test_email.py your-email@example.com
```

### 2. Check spam folder if you don't see it

### 3. Once working, test full flow:
- Forgot password → Receive email → Click link → Reset password
- Forgot username → Receive email → See username
- Admin creates user → User receives welcome email

---

## 💰 SENDGRID PRICING

### Free Plan (Perfect for you):
- ✅ 100 emails/day
- ✅ Email validation
- ✅ Basic analytics
- ✅ 1 sender email address

### If you need more:
- **Essentials**: $19.95/month → 50,000 emails/month
- **Pro**: $89.95/month → 1.5 million emails/month

**For password resets**: Free plan is MORE than enough!

---

## ⚠️ IMPORTANT NOTES

### 1. Sender Email Verification:
- **MUST** verify `noreply@saveenergysystems.com`
- Can't send emails until verified
- Check your email inbox!

### 2. API Key Security:
- **NEVER** commit API key to GitHub
- Keep it in `.env` file
- Add `.env` to `.gitignore`

### 3. Rate Limiting:
- Free plan: 100 emails/day
- Enough for password resets
- Upgrade if you need more

### 4. Email Deliverability:
- Emails might go to spam initially
- Use proper "From" address
- Don't send too many at once

---

## 🚀 READY TO SET THIS UP?

**Next Steps:**

1. **You do**: Create SendGrid account + get API key (10 minutes)
2. **I do**: Build email service in backend (30 minutes)
3. **I do**: Create forgot password/username pages (30 minutes)
4. **I do**: Build backend APIs for password reset (30 minutes)
5. **We test**: Send test emails (10 minutes)

---

## 🎯 LET'S START!

**Tell me when you have:**
1. ✅ SendGrid account created
2. ✅ API Key copied (starts with `SG.`)
3. ✅ Sender email verified (`noreply@saveenergysystems.com`)

**Then I'll build:**
- Email service
- Forgot password page
- Forgot username page
- Backend APIs
- Test everything

---

**Questions?**
- Need help with SendGrid signup?
- Want me to build this now with a placeholder API key?
- Ready to give me your API key?

Let me know! 🚀
