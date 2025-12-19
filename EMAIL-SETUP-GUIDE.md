# 📧 EMAIL SYSTEM SETUP GUIDE
## SendGrid Integration for PF Resource Hub

---

## 🎯 WHAT WE'RE BUILDING

### Email Types:
1. **Welcome Email** - New user created (with temp password)
2. **Password Reset** - User/admin resets password
3. **Username Recovery** - User forgot username
4. **Account Notifications** - Deactivation, activation, etc.

---

## 📋 STEP 1: GET SENDGRID API KEY

### Go to SendGrid:
1. **Sign up**: https://signup.sendgrid.com/
2. **Free Plan**: 100 emails/day (enough for testing)
3. **Paid Plan**: $19.95/month = 50,000 emails/month

### Create API Key:
1. Login to SendGrid
2. Go to **Settings** → **API Keys**
3. Click **"Create API Key"**
4. Name: `pf-resource-hub-api`
5. Permissions: **"Full Access"**
6. Copy the API key (starts with `SG.`)

**⚠️ IMPORTANT**: Save this key! You can't see it again.

---

## 📋 STEP 2: VERIFY SENDER EMAIL

SendGrid requires you to verify the email address that sends emails.

### Single Sender Verification (Quick - 5 minutes):
1. Go to **Settings** → **Sender Authentication**
2. Click **"Verify a Single Sender"**
3. Fill in the form:
   - **From Name**: `PF Resource Hub`
   - **From Email**: `noreply@saveenergysystems.com` (or your domain)
   - **Reply To**: `support@saveenergysystems.com`
   - **Company Address**: Your SES address
4. Click **"Create"**
5. **Check your email** and click verification link

### Domain Authentication (Production - Better):
1. Go to **Settings** → **Sender Authentication**
2. Click **"Authenticate Your Domain"**
3. Enter your domain: `saveenergysystems.com`
4. Add DNS records to your domain (SendGrid provides them)
5. Wait for verification (24-48 hours)

---

## 📋 STEP 3: ADD API KEY TO BACKEND

### Update `.env` file:

```bash
cd /home/user/pf-resource-hub/backend
```

Add to `.env`:
```bash
# SendGrid Email Configuration
SENDGRID_API_KEY=SG.your_actual_api_key_here
SENDGRID_FROM_EMAIL=noreply@saveenergysystems.com
SENDGRID_FROM_NAME=PF Resource Hub
SENDGRID_REPLY_TO=support@saveenergysystems.com

# Email Settings
EMAIL_MODE=live  # Change from 'console' to 'live'
```

---

## 📋 STEP 4: INSTALL SENDGRID PYTHON LIBRARY

```bash
cd /home/user/pf-resource-hub/backend
pip install sendgrid
```

---

## 📋 STEP 5: CREATE EMAIL SERVICE

Create new file: `backend/email_service.py`

```python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import secrets
import string

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@saveenergysystems.com')
        self.from_name = os.getenv('SENDGRID_FROM_NAME', 'PF Resource Hub')
        self.reply_to = os.getenv('SENDGRID_REPLY_TO', 'support@saveenergysystems.com')
        self.mode = os.getenv('EMAIL_MODE', 'console')
        
    def generate_password(self, length=12):
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        return f"PF-{password[:4]}{secrets.choice('!@#$')}{password[4:8]}"
    
    def send_email(self, to_email, subject, html_content, text_content=None):
        """Send an email via SendGrid"""
        if self.mode == 'console':
            print(f"\n{'='*60}")
            print(f"📧 EMAIL (Console Mode)")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"\n{html_content}\n")
            print(f"{'='*60}\n")
            return True
            
        try:
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                message.add_content(Content("text/plain", text_content))
            
            message.reply_to = Email(self.reply_to)
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Email sent to {to_email}")
                return True
            else:
                print(f"❌ Email failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
            return False
    
    def send_welcome_email(self, user_name, user_email, temp_password):
        """Send welcome email to new user"""
        subject = "Welcome to PF Resource Hub"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #7B2FE4 0%, #1A0933 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .credentials {{ background: white; padding: 20px; border-radius: 8px; 
                               border-left: 4px solid #7B2FE4; margin: 20px 0; }}
                .button {{ display: inline-block; background: #FFC107; color: #1A0933; 
                          padding: 15px 30px; text-decoration: none; border-radius: 8px; 
                          font-weight: bold; margin: 20px 0; }}
                .warning {{ background: #FFF3CD; border-left: 4px solid #FFC107; 
                           padding: 15px; margin: 20px 0; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to PF Resource Hub!</h1>
                </div>
                <div class="content">
                    <p>Hi {user_name},</p>
                    
                    <p>Your account has been created for the <strong>Planet Fitness & Save Energy Systems Resource Hub</strong>.</p>
                    
                    <div class="credentials">
                        <h3>🔐 Your Login Credentials</h3>
                        <p><strong>Email:</strong> {user_email}</p>
                        <p><strong>Temporary Password:</strong> <code>{temp_password}</code></p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://pf-resource-hub.pages.dev" class="button">
                            Login Now →
                        </a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ IMPORTANT:</strong>
                        <ul>
                            <li>You will be required to change your password on first login</li>
                            <li>Keep this email safe - you'll need the temporary password to login</li>
                            <li>If you have any issues, contact your administrator</li>
                        </ul>
                    </div>
                    
                    <h3>What you can do:</h3>
                    <ul>
                        <li>🔍 Search HVAC documentation with Steph Assistant</li>
                        <li>📞 Access emergency contacts and protocols</li>
                        <li>🛠️ Order replacement parts</li>
                        <li>📚 Browse SES resources and guides</li>
                        <li>💼 Submit work orders and service requests</li>
                    </ul>
                    
                    <p>Need help? Contact us at <a href="mailto:{self.reply_to}">{self.reply_to}</a></p>
                    
                    <p>Best regards,<br>
                    <strong>PF Resource Hub Team</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to PF Resource Hub!
        
        Hi {user_name},
        
        Your account has been created.
        
        Login Credentials:
        Email: {user_email}
        Temporary Password: {temp_password}
        
        Login at: https://pf-resource-hub.pages.dev
        
        IMPORTANT: Change your password on first login.
        
        Need help? Email {self.reply_to}
        
        Best regards,
        PF Resource Hub Team
        """
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def send_password_reset_email(self, user_name, user_email, new_password):
        """Send password reset email"""
        subject = "Your Password Has Been Reset"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #7B2FE4 0%, #1A0933 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .credentials {{ background: white; padding: 20px; border-radius: 8px; 
                               border-left: 4px solid #DC2626; margin: 20px 0; }}
                .button {{ display: inline-block; background: #FFC107; color: #1A0933; 
                          padding: 15px 30px; text-decoration: none; border-radius: 8px; 
                          font-weight: bold; margin: 20px 0; }}
                .warning {{ background: #FEE2E2; border-left: 4px solid #DC2626; 
                           padding: 15px; margin: 20px 0; border-radius: 4px; color: #991B1B; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔑 Password Reset</h1>
                </div>
                <div class="content">
                    <p>Hi {user_name},</p>
                    
                    <p>Your password has been reset by an administrator.</p>
                    
                    <div class="credentials">
                        <h3>🔐 Your New Temporary Password</h3>
                        <p><strong>Password:</strong> <code>{new_password}</code></p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://pf-resource-hub.pages.dev" class="button">
                            Login Now →
                        </a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ SECURITY NOTICE:</strong>
                        <ul>
                            <li><strong>Change your password immediately</strong> after logging in</li>
                            <li>This temporary password should only be used once</li>
                            <li>If you didn't request this reset, contact your administrator immediately</li>
                        </ul>
                    </div>
                    
                    <p>Need help? Contact us at <a href="mailto:{self.reply_to}">{self.reply_to}</a></p>
                    
                    <p>Best regards,<br>
                    <strong>PF Resource Hub Team</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset
        
        Hi {user_name},
        
        Your password has been reset.
        
        New Temporary Password: {new_password}
        
        Login at: https://pf-resource-hub.pages.dev
        
        SECURITY: Change your password immediately after logging in.
        
        Need help? Email {self.reply_to}
        
        Best regards,
        PF Resource Hub Team
        """
        
        return self.send_email(user_email, subject, html_content, text_content)
    
    def send_username_recovery_email(self, user_name, user_email):
        """Send username recovery email"""
        subject = "Your Username Recovery"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #7B2FE4 0%, #1A0933 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .credentials {{ background: white; padding: 20px; border-radius: 8px; 
                               border-left: 4px solid #7B2FE4; margin: 20px 0; }}
                .button {{ display: inline-block; background: #FFC107; color: #1A0933; 
                          padding: 15px 30px; text-decoration: none; border-radius: 8px; 
                          font-weight: bold; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>👤 Username Recovery</h1>
                </div>
                <div class="content">
                    <p>Hi {user_name},</p>
                    
                    <p>You requested to recover your username for the PF Resource Hub.</p>
                    
                    <div class="credentials">
                        <h3>📧 Your Username (Email)</h3>
                        <p><strong>Username:</strong> {user_email}</p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://pf-resource-hub.pages.dev" class="button">
                            Login Now →
                        </a>
                    </div>
                    
                    <p><strong>Forgot your password?</strong><br>
                    Use the "Forgot Password" link on the login page.</p>
                    
                    <p>Need help? Contact us at <a href="mailto:{self.reply_to}">{self.reply_to}</a></p>
                    
                    <p>Best regards,<br>
                    <strong>PF Resource Hub Team</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Username Recovery
        
        Hi {user_name},
        
        Your username: {user_email}
        
        Login at: https://pf-resource-hub.pages.dev
        
        Forgot password? Use "Forgot Password" on login page.
        
        Need help? Email {self.reply_to}
        
        Best regards,
        PF Resource Hub Team
        """
        
        return self.send_email(user_email, subject, html_content, text_content)


# Create singleton instance
email_service = EmailService()
```

---

## 📋 STEP 6: TEST EMAIL SERVICE

Create test file: `backend/test_email.py`

```python
from email_service import email_service

# Test 1: Welcome Email
print("Testing Welcome Email...")
email_service.send_welcome_email(
    user_name="Test User",
    user_email="your-email@example.com",  # YOUR REAL EMAIL
    temp_password="PF-xK9m!vR4"
)

# Test 2: Password Reset
print("\nTesting Password Reset Email...")
email_service.send_password_reset_email(
    user_name="Test User",
    user_email="your-email@example.com",  # YOUR REAL EMAIL
    new_password="PF-aB7x!mN3"
)

# Test 3: Username Recovery
print("\nTesting Username Recovery Email...")
email_service.send_username_recovery_email(
    user_name="Test User",
    user_email="your-email@example.com"  # YOUR REAL EMAIL
)

print("\n✅ All tests complete! Check your email.")
```

Run test:
```bash
cd /home/user/pf-resource-hub/backend
python test_email.py
```

---

## 📋 STEP 7: INTEGRATE WITH EXISTING AUTH ROUTES

Update `backend/app.py` to use email service:

```python
from email_service import email_service

# Password reset endpoint
@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    
    # Find user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Generate new password
    new_password = email_service.generate_password()
    
    # Hash and save
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.force_password_change = True
    db.session.commit()
    
    # Send email
    email_sent = email_service.send_password_reset_email(
        user_name=user.name or user.email.split('@')[0],
        user_email=user.email,
        new_password=new_password
    )
    
    return jsonify({
        'success': True,
        'message': 'Password reset email sent',
        'email_sent': email_sent
    })

# Username recovery endpoint
@app.route('/api/auth/recover-username', methods=['POST'])
def recover_username():
    data = request.get_json()
    # Could use name, phone, or other identifier
    name = data.get('name')
    
    # Find user by name (you might want better search)
    user = User.query.filter(User.name.ilike(f'%{name}%')).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Send email
    email_sent = email_service.send_username_recovery_email(
        user_name=user.name or user.email.split('@')[0],
        user_email=user.email
    )
    
    return jsonify({
        'success': True,
        'message': 'Username recovery email sent',
        'email_sent': email_sent
    })
```

---

## ✅ TESTING CHECKLIST

### Console Mode (First):
- [ ] Set `EMAIL_MODE=console` in `.env`
- [ ] Run `python test_email.py`
- [ ] Check terminal output
- [ ] Verify email HTML looks good

### Live Mode (Second):
- [ ] Get SendGrid API key
- [ ] Verify sender email
- [ ] Add API key to `.env`
- [ ] Set `EMAIL_MODE=live`
- [ ] Run `python test_email.py` with YOUR email
- [ ] Check your inbox
- [ ] Check spam folder if not received

---

## 🚀 QUICK START (5 MINUTES)

```bash
# 1. Get API key from SendGrid (sign up free)
# 2. Add to .env
cd /home/user/pf-resource-hub/backend
echo 'SENDGRID_API_KEY=SG.your_key_here' >> .env
echo 'EMAIL_MODE=live' >> .env

# 3. Install SendGrid
pip install sendgrid

# 4. Create email_service.py (use code above)

# 5. Test it
python test_email.py
```

---

## 💰 COST

- **Free**: 100 emails/day
- **Essentials**: $19.95/month = 50,000 emails
- **Pro**: $89.95/month = 100,000 emails

For your use case: **Free tier is fine** for now!

---

## 🎯 NEXT STEPS

Want me to:
1. **Create these files now?** (email_service.py, test_email.py)
2. **Help you get SendGrid API key?** (guide you through signup)
3. **Remove location filtering from PF Admin?** (show ALL users)

What do you want to do first?
