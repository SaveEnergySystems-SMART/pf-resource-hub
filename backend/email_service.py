"""
Email Service for PF Resource Hub
Handles all email notifications using SendGrid
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
import secrets
import string
from datetime import datetime, timedelta

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY', 'YOUR_SENDGRID_API_KEY_HERE')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@saveenergysystems.com')
        self.from_name = os.getenv('SENDGRID_FROM_NAME', 'PF Resource Hub')
        self.frontend_url = os.getenv('FRONTEND_URL', 'https://pf-resource-hub.pages.dev')
        
        # Initialize SendGrid client
        if self.api_key != 'YOUR_SENDGRID_API_KEY_HERE':
            self.client = SendGridAPIClient(self.api_key)
        else:
            self.client = None
            print("⚠️  SendGrid API key not configured. Emails will be printed to console only.")
    
    def _send_email(self, to_email, subject, html_content, plain_text_content):
        """
        Send email via SendGrid or print to console if not configured
        """
        if not self.client:
            # Email not configured - print to console for testing
            print("\n" + "="*60)
            print("📧 EMAIL NOTIFICATION (SendGrid not configured)")
            print("="*60)
            print(f"To: {to_email}")
            print(f"From: {self.from_name} <{self.from_email}>")
            print(f"Subject: {subject}")
            print("-"*60)
            print(plain_text_content)
            print("="*60 + "\n")
            return {"success": True, "mode": "console", "message": "Email printed to console (SendGrid not configured)"}
        
        try:
            # Create email message
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", plain_text_content),
                html_content=Content("text/html", html_content)
            )
            
            # Send email
            response = self.client.send(message)
            
            return {
                "success": True,
                "mode": "sendgrid",
                "status_code": response.status_code,
                "message": f"Email sent successfully to {to_email}"
            }
        
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_password_reset_email(self, to_email, reset_token, user_name=None):
        """
        Send password reset email with reset link
        Token expires in 1 hour
        """
        reset_link = f"{self.frontend_url}/reset-password.html?token={reset_token}"
        
        greeting = f"Hi {user_name}," if user_name else "Hi,"
        
        # Plain text version
        plain_text = f"""{greeting}

You requested to reset your password for the PF Resource Hub.

Click this link to reset your password:
{reset_link}

⏰ This link expires in 1 hour.

If you didn't request this, please ignore this email. Your password will remain unchanged.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
"""
        
        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #7B2FE4;">Reset Your Password</h2>
                <p>{greeting}</p>
                <p>You requested to reset your password for the <strong>PF Resource Hub</strong>.</p>
                <p>Click the button below to reset your password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background-color: #7B2FE4; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        Reset Password
                    </a>
                </div>
                <p style="color: #666; font-size: 14px;">
                    ⏰ This link expires in 1 hour.
                </p>
                <p style="color: #666; font-size: 14px;">
                    Or copy and paste this link into your browser:<br>
                    <a href="{reset_link}" style="color: #7B2FE4;">{reset_link}</a>
                </p>
                <p style="color: #666; font-size: 14px;">
                    If you didn't request this, please ignore this email. Your password will remain unchanged.
                </p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #999; font-size: 12px;">
                    PF Resource Hub Team<br>
                    Support: support@saveenergysystems.com
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email=to_email,
            subject="Reset Your PF Resource Hub Password",
            html_content=html_content,
            plain_text_content=plain_text
        )
    
    def send_username_recovery_email(self, to_email, username, user_name=None):
        """
        Send username recovery email
        """
        login_link = f"{self.frontend_url}/login-final.html"
        
        greeting = f"Hi {user_name}," if user_name else "Hi,"
        
        # Plain text version
        plain_text = f"""{greeting}

You requested your username for the PF Resource Hub.

Your login email is: {username}

You can login here:
{login_link}

If you didn't request this, please ignore this email.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
"""
        
        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #7B2FE4;">Your Username Recovery</h2>
                <p>{greeting}</p>
                <p>You requested your username for the <strong>PF Resource Hub</strong>.</p>
                <div style="background-color: #f5f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666;">Your login email:</p>
                    <p style="margin: 10px 0 0 0; font-size: 18px; font-weight: bold; color: #1A0933;">
                        {username}
                    </p>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{login_link}" 
                       style="background-color: #7B2FE4; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        Login Now
                    </a>
                </div>
                <p style="color: #666; font-size: 14px;">
                    If you didn't request this, please ignore this email.
                </p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #999; font-size: 12px;">
                    PF Resource Hub Team<br>
                    Support: support@saveenergysystems.com
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email=to_email,
            subject="Your PF Resource Hub Username",
            html_content=html_content,
            plain_text_content=plain_text
        )
    
    def send_welcome_email(self, to_email, user_name, temp_password):
        """
        Send welcome email to new user with temporary password
        """
        login_link = f"{self.frontend_url}/login-final.html"
        
        # Plain text version
        plain_text = f"""Hi {user_name},

Welcome to the PF Resource Hub!

Your account has been created. Here are your login details:

Email: {to_email}
Temporary Password: {temp_password}

Login here: {login_link}

⚠️ IMPORTANT: You will be required to change your password on your first login.

What you can do:
• Access HVAC troubleshooting guides
• Order parts and equipment
• View SES protocols and resources
• Get emergency support 24/7

Need help? Contact your administrator or email support@saveenergysystems.com

---
PF Resource Hub Team
Support: support@saveenergysystems.com
"""
        
        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #7B2FE4;">Welcome to PF Resource Hub! 🎉</h2>
                <p>Hi {user_name},</p>
                <p>Your account has been created for the <strong>PF Resource Hub</strong>!</p>
                
                <div style="background-color: #f5f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1A0933;">Your Login Details:</h3>
                    <p style="margin: 10px 0;">
                        <strong>Email:</strong> {to_email}<br>
                        <strong>Temporary Password:</strong> <code style="background: white; padding: 4px 8px; border-radius: 4px;">{temp_password}</code>
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{login_link}" 
                       style="background-color: #7B2FE4; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        Login Now
                    </a>
                </div>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #FFC107; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; color: #856404;">
                        ⚠️ <strong>Important:</strong> You will be required to change your password on your first login.
                    </p>
                </div>
                
                <h3 style="color: #1A0933;">What you can do:</h3>
                <ul style="color: #666;">
                    <li>Access HVAC troubleshooting guides</li>
                    <li>Order parts and equipment</li>
                    <li>View SES protocols and resources</li>
                    <li>Get emergency support 24/7</li>
                </ul>
                
                <p style="color: #666; font-size: 14px;">
                    Need help? Contact your administrator or email support@saveenergysystems.com
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #999; font-size: 12px;">
                    PF Resource Hub Team<br>
                    Support: support@saveenergysystems.com
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email=to_email,
            subject="Welcome to PF Resource Hub - Your Login Details",
            html_content=html_content,
            plain_text_content=plain_text
        )
    
    def send_admin_password_reset_email(self, to_email, user_name, new_temp_password):
        """
        Send email when admin resets a user's password
        """
        login_link = f"{self.frontend_url}/login-final.html"
        
        # Plain text version
        plain_text = f"""Hi {user_name},

Your password has been reset by an administrator.

Your new temporary password is: {new_temp_password}

Login here: {login_link}

⚠️ IMPORTANT: Change your password immediately after logging in.

If you didn't request this reset, please contact your administrator immediately.

---
PF Resource Hub Team
Support: support@saveenergysystems.com
"""
        
        # HTML version
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #7B2FE4;">Your Password Has Been Reset</h2>
                <p>Hi {user_name},</p>
                <p>Your password has been reset by an administrator.</p>
                
                <div style="background-color: #f5f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666;">Your new temporary password:</p>
                    <p style="margin: 10px 0 0 0; font-size: 18px; font-weight: bold; color: #1A0933;">
                        <code style="background: white; padding: 8px 12px; border-radius: 4px;">{new_temp_password}</code>
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{login_link}" 
                       style="background-color: #7B2FE4; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        Login Now
                    </a>
                </div>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #FFC107; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; color: #856404;">
                        ⚠️ <strong>Important:</strong> Change your password immediately after logging in.
                    </p>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    If you didn't request this reset, please contact your administrator immediately.
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                <p style="color: #999; font-size: 12px;">
                    PF Resource Hub Team<br>
                    Support: support@saveenergysystems.com
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(
            to_email=to_email,
            subject="Your Password Has Been Reset - PF Resource Hub",
            html_content=html_content,
            plain_text_content=plain_text
        )


# Utility Functions
def generate_secure_password(length=12):
    """
    Generate a secure random password
    Format: PF-xK9m!vR4
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    # Add special character and format
    return f"PF-{password[:4]}{secrets.choice('!@#$')}{password[4:8]}"


def generate_reset_token():
    """
    Generate a secure reset token for password resets
    Returns a URL-safe token
    """
    return secrets.token_urlsafe(32)


# Example usage
if __name__ == "__main__":
    email_service = EmailService()
    
    # Test password generation
    print("\n🔐 Generated Password:", generate_secure_password())
    print("🔑 Generated Reset Token:", generate_reset_token())
    
    # Test emails (will print to console if SendGrid not configured)
    print("\n📧 Testing Email Service...")
    
    # Test 1: Password reset
    email_service.send_password_reset_email(
        to_email="test@example.com",
        reset_token=generate_reset_token(),
        user_name="John Smith"
    )
    
    # Test 2: Username recovery
    email_service.send_username_recovery_email(
        to_email="test@example.com",
        username="john.smith@planetfitness.com",
        user_name="John Smith"
    )
    
    # Test 3: Welcome email
    email_service.send_welcome_email(
        to_email="test@example.com",
        user_name="John Smith",
        temp_password=generate_secure_password()
    )
    
    # Test 4: Admin password reset
    email_service.send_admin_password_reset_email(
        to_email="test@example.com",
        user_name="John Smith",
        new_temp_password=generate_secure_password()
    )
    
    print("\n✅ Email service tests complete!")


def send_username_recovery_email(to_email, username, first_name):
    """Send username recovery email using EmailService"""
    email_service = EmailService()
    
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
                <p>Hi {first_name},</p>
                
                <p>You requested to recover your username for the PF Resource Hub.</p>
                
                <div class="credentials">
                    <h3>📧 Your Username (Email)</h3>
                    <p><strong>Username:</strong> {username}</p>
                </div>
                
                <div style="text-align: center;">
                    <a href="https://pf-resource-hub.pages.dev" class="button">
                        Login Now →
                    </a>
                </div>
                
                <p><strong>Forgot your password?</strong><br>
                Use the "Forgot Password" link on the login page.</p>
                
                <p>Need help? Contact us at support@saveenergysystems.com</p>
                
                <p>Best regards,<br>
                <strong>PF Resource Hub Team</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_text = f"""
    Username Recovery
    
    Hi {first_name},
    
    Your username for PF Resource Hub: {username}
    
    Login at: https://pf-resource-hub.pages.dev
    
    Forgot your password? Use "Forgot Password" on the login page.
    
    Best regards,
    PF Resource Hub Team
    """
    
    return email_service._send_email(to_email, "Your Username Recovery", html_content, plain_text)


def generate_secure_password(length=12):
    """Generate a secure random password"""
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return f"PF-{password[:4]}{secrets.choice('!@#$')}{password[4:8]}"


# Module-level wrapper functions for app.py imports
_email_service = EmailService()

def send_welcome_email(to_email, user_name, temp_password):
    """Wrapper for EmailService.send_welcome_email"""
    return _email_service.send_welcome_email(to_email, user_name, temp_password)

def send_password_reset_email(to_email, reset_token, user_name=None):
    """Wrapper for EmailService.send_password_reset_email"""
    return _email_service.send_password_reset_email(to_email, reset_token, user_name)

def send_username_reminder_email(to_email, username, user_name=None):
    """Wrapper for EmailService.send_username_recovery_email"""
    return _email_service.send_username_recovery_email(to_email, username, user_name)

def send_password_changed_email(to_email, user_name):
    """Send notification when password is changed"""
    # Simple notification - you can enhance this later
    plain_text = f"Hi {user_name}, your password was changed successfully."
    html_content = f"<p>Hi {user_name},</p><p>Your password was changed successfully.</p>"
    return _email_service._send_email(to_email, "Password Changed", html_content, plain_text)

def send_admin_password_reset_email(to_email, user_name, new_temp_password):
    """Wrapper for EmailService.send_admin_password_reset_email"""
    return _email_service.send_admin_password_reset_email(to_email, user_name, new_temp_password)

def send_account_deactivated_email(to_email, user_name):
    """Send notification when account is deactivated"""
    plain_text = f"Hi {user_name}, your account has been deactivated. Contact your administrator for assistance."
    html_content = f"<p>Hi {user_name},</p><p>Your account has been deactivated. Contact your administrator for assistance.</p>"
    return _email_service._send_email(to_email, "Account Deactivated", html_content, plain_text)
