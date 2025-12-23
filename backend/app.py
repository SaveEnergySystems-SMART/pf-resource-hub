# Planet Fitness Resource Hub - Backend API
# Complete Flask application with authentication, user management, and admin dashboards

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
import os

# Import config and models
from config import config, Config
from models import db, User, PasswordReset, ActivityLog, Session
from email_service import (
    send_welcome_email,
    send_password_reset_email,
    send_username_reminder_email,
    send_password_changed_email,
    send_admin_password_reset_email,
    send_account_deactivated_email
)
from openai_service import get_ai_response
from analytics_service import get_all_analytics_data

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
CORS(app, 
     resources={r"/*": {"origins": "*"}},  # Allow all origins for now
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
db.init_app(app)

# =============================================================================
# AUTO-INITIALIZE DATABASE ON STARTUP
# =============================================================================

def ensure_database_initialized():
    """Ensure database is initialized (runs on app startup, even with Gunicorn)"""
    try:
        with app.app_context():
            # Try to query users table
            User.query.first()
            print("✅ Database already initialized")
    except Exception as e:
        print(f"⚠️ Database not initialized, creating tables: {e}")
        with app.app_context():
            db.create_all()
            
            # Create default admin users
            ses_admin = User.query.filter_by(email=Config.SES_SUPER_ADMIN_EMAIL).first()
            if not ses_admin:
                ses_admin = User(
                    username='asoler',
                    email=Config.SES_SUPER_ADMIN_EMAIL,
                    first_name='Adriana',
                    last_name='Soler',
                    role='ses_admin',
                    is_active=True
                )
                ses_admin.set_password('SES-Admin-2025!')
                db.session.add(ses_admin)
                print(f"✅ Created SES Super Admin: {ses_admin.email}")
            
            pf_admin = User.query.filter_by(email=Config.PF_ADMIN_TEST_EMAIL).first()
            if not pf_admin:
                pf_admin = User(
                    username='pfadmin',
                    email=Config.PF_ADMIN_TEST_EMAIL,
                    first_name='Adriana',
                    last_name='Test Admin',
                    role='pf_admin',
                    location='Boston Region',
                    is_active=True,
                    created_by_id=ses_admin.id if ses_admin else None
                )
                pf_admin.set_password('PF-Admin-2025!')
                db.session.add(pf_admin)
                print(f"✅ Created PF Test Admin: {pf_admin.email}")
            
            db.session.commit()
            print("✅ Database initialized successfully!")

# Run database initialization check on module load
ensure_database_initialized()

# =============================================================================
# AUTHENTICATION DECORATORS
# =============================================================================

def token_required(f):
    """Require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
            
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            # Update last activity
            current_user.last_login = datetime.utcnow()
            db.session.commit()
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """Require admin role (ses_admin or pf_admin)"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role not in ['ses_admin', 'pf_admin']:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


def ses_admin_required(f):
    """Require SES admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'ses_admin':
            return jsonify({'error': 'SES admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def log_activity(user_id, action, description=None, metadata=None):
    """Log user activity"""
    try:
        log = ActivityLog(
            user_id=user_id,
            action=action,
            description=description,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            metadata=metadata
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")


def generate_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


# =============================================================================
# AUTHENTICATION ENDPOINTS
# =============================================================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user or not user.check_password(password):
            log_activity(user.id if user else None, 'login_failed', f'Invalid credentials for {username}')
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            log_activity(user.id, 'login_failed', 'Account deactivated')
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Generate token
        token = generate_jwt_token(user)
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log successful login
        log_activity(user.id, 'login', f'Successful login')
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout"""
    try:
        log_activity(current_user.id, 'logout', 'User logged out')
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        print(f"🔍 [FORGOT-PASSWORD] Request received for email: {email}")
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        # Always return success (security best practice)
        if not user:
            print(f"⚠️ [FORGOT-PASSWORD] User not found for email: {email}")
            return jsonify({'message': 'If email exists, reset link sent'}), 200
        
        print(f"✅ [FORGOT-PASSWORD] User found: {user.email} (ID: {user.id})")
        
        # Generate reset token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        print(f"🔍 [FORGOT-PASSWORD] Creating token: {token[:15]}...")
        print(f"🔍 [FORGOT-PASSWORD] Token expires at: {expires_at}")
        
        password_reset = PasswordReset(
            token=token,
            user_id=user.id,
            expires_at=expires_at,
            ip_address=request.remote_addr
        )
        db.session.add(password_reset)
        
        # Force immediate commit and flush
        try:
            db.session.flush()
            db.session.commit()
            print(f"✅ [FORGOT-PASSWORD] Token saved to database successfully")
            
            # Verify it was actually saved
            verification = PasswordReset.query.filter_by(token=token).first()
            if verification:
                print(f"✅ [FORGOT-PASSWORD] Token verified in database: {verification.token[:15]}...")
            else:
                print(f"❌ [FORGOT-PASSWORD] WARNING: Token not found in database after commit!")
                
        except Exception as db_error:
            print(f"❌ [FORGOT-PASSWORD] Database error: {str(db_error)}")
            db.session.rollback()
            raise
        
        # Send email
        reset_link = f"{app.config['FRONTEND_URL']}/reset-password.html?token={token}"
        send_password_reset_email(user.email, reset_link, user.first_name)
        print(f"📧 [FORGOT-PASSWORD] Reset email sent to: {user.email}")
        
        log_activity(user.id, 'password_reset_requested', 'Password reset email sent')
        
        return jsonify({'message': 'If email exists, reset link sent'}), 200
        
    except Exception as e:
        print(f"❌ [FORGOT-PASSWORD] Exception: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/forgot-username', methods=['POST'])
def forgot_username():
    """Request username reminder"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'message': 'If email exists, username sent'}), 200
        
        # Send email
        send_username_reminder_email(user.email, user.username, user.first_name)
        
        log_activity(user.id, 'username_reminder_requested', 'Username reminder email sent')
        
        return jsonify({'message': 'If email exists, username sent'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        print(f"🔍 [RESET-PASSWORD] Request received")
        print(f"🔍 [RESET-PASSWORD] Token received: {token[:15] if token else 'NONE'}...")
        print(f"🔍 [RESET-PASSWORD] Password received: {'YES' if new_password else 'NO'}")
        
        if not token or not new_password:
            print(f"❌ [RESET-PASSWORD] Missing token or password")
            return jsonify({'error': 'Token and password required'}), 400
        
        # Find valid token
        print(f"🔍 [RESET-PASSWORD] Searching for token in database...")
        password_reset = PasswordReset.query.filter_by(token=token, used=False).first()
        
        if not password_reset:
            print(f"❌ [RESET-PASSWORD] Token not found in database!")
            
            # Debug: Check if token exists at all (even if used)
            any_token = PasswordReset.query.filter_by(token=token).first()
            if any_token:
                print(f"⚠️ [RESET-PASSWORD] Token exists but marked as USED at {any_token.used_at}")
            else:
                print(f"❌ [RESET-PASSWORD] Token does NOT exist in database at all!")
                
                # Debug: Show all tokens in database
                all_tokens = PasswordReset.query.order_by(PasswordReset.created_at.desc()).limit(5).all()
                print(f"🔍 [RESET-PASSWORD] Last 5 tokens in database:")
                for t in all_tokens:
                    print(f"   - {t.token[:15]}... (used={t.used}, expires={t.expires_at})")
            
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        print(f"✅ [RESET-PASSWORD] Token found in database!")
        print(f"🔍 [RESET-PASSWORD] Token user_id: {password_reset.user_id}")
        print(f"🔍 [RESET-PASSWORD] Token expires_at: {password_reset.expires_at}")
        print(f"🔍 [RESET-PASSWORD] Token used: {password_reset.used}")
        print(f"🔍 [RESET-PASSWORD] Current time: {datetime.utcnow()}")
        
        # Check if valid
        if not password_reset.is_valid():
            print(f"❌ [RESET-PASSWORD] Token is NOT VALID (expired or used)")
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        print(f"✅ [RESET-PASSWORD] Token is VALID!")
        
        # Update password
        user = password_reset.user
        print(f"✅ [RESET-PASSWORD] Updating password for user: {user.email}")
        user.set_password(new_password)
        
        # Mark token as used
        password_reset.used = True
        password_reset.used_at = datetime.utcnow()
        
        db.session.commit()
        print(f"✅ [RESET-PASSWORD] Password updated successfully!")
        
        # Send confirmation email
        send_password_changed_email(user.email, user.first_name)
        
        log_activity(user.id, 'password_reset', 'Password reset successfully')
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        print(f"❌ [RESET-PASSWORD] Exception: {str(e)}")
        import traceback
        print(f"❌ [RESET-PASSWORD] Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

        
        # Find valid token
        password_reset = PasswordReset.query.filter_by(token=token, used=False).first()
        
        if not password_reset or not password_reset.is_valid():
            return jsonify({'error': 'Invalid or expired token'}), 400
        
        # Update password
        user = password_reset.user
        user.set_password(new_password)
        
        # Mark token as used
        password_reset.used = True
        password_reset.used_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send confirmation email
        send_password_changed_email(user.email, user.first_name)
        
        log_activity(user.id, 'password_reset', 'Password reset successfully')
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change password for authenticated user"""
    try:
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': 'Old and new password required'}), 400
        
        if not current_user.check_password(old_password):
            return jsonify({'error': 'Current password incorrect'}), 401
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        # Send confirmation email
        send_password_changed_email(current_user.email, current_user.first_name)
        
        log_activity(current_user.id, 'password_changed', 'Password changed by user')
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================================================
# USER MANAGEMENT ENDPOINTS
# =============================================================================

@app.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    """Get list of users (filtered by role)"""
    try:
        query = User.query
        
        # PF admins can only see GMs from their location
        if current_user.role == 'pf_admin':
            query = query.filter_by(role='gm')
            if current_user.location:
                query = query.filter_by(location=current_user.location)
        
        users = query.order_by(User.created_at.desc()).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['POST'])
@token_required
@admin_required
def create_user(current_user):
    """Create new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate role permissions
        if current_user.role == 'pf_admin' and data['role'] != 'gm':
            return jsonify({'error': 'PF admins can only create GM accounts'}), 403
        
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            phone=data.get('phone', ''),
            location=data.get('location', ''),
            created_by_id=current_user.id
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user.email, user.first_name, data['password'])
        
        log_activity(current_user.id, 'user_created', f'Created user: {user.username}')
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user, user_id):
    """Update user information"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # PF admins can only update GMs
        if current_user.role == 'pf_admin' and user.role != 'gm':
            return jsonify({'error': 'Permission denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'location' in data:
            user.location = data['location']
        
        # Only SES admins can change active status
        if 'is_active' in data and current_user.role == 'ses_admin':
            user.is_active = data['is_active']
        
        db.session.commit()
        
        log_activity(current_user.id, 'user_updated', f'Updated user: {user.username}')
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
@token_required
@admin_required
def admin_reset_password(current_user, user_id):
    """Admin resets user password"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # PF admins can only reset GM passwords
        if current_user.role == 'pf_admin' and user.role != 'gm':
            return jsonify({'error': 'Permission denied'}), 403
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(12)
        user.set_password(temp_password)
        db.session.commit()
        
        # Send email
        admin_name = f"{current_user.first_name} {current_user.last_name}"
        send_admin_password_reset_email(
            user.email,
            user.username,
            temp_password,
            user.first_name,
            admin_name
        )
        
        log_activity(current_user.id, 'admin_password_reset', f'Reset password for: {user.username}')
        
        return jsonify({
            'message': 'Password reset successfully',
            'temp_password': temp_password
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@ses_admin_required
def delete_user(current_user, user_id):
    """Delete user (SES admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.id == current_user.id:
            return jsonify({'error': 'Cannot delete yourself'}), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        log_activity(current_user.id, 'user_deleted', f'Deleted user: {username}')
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# =============================================================================
# ACTIVITY LOGS
# =============================================================================

@app.route('/api/activity-logs', methods=['GET'])
@token_required
@admin_required
def get_activity_logs(current_user):
    """Get activity logs (filtered by role)"""
    try:
        query = ActivityLog.query
        
        # PF admins can only see logs from their users
        if current_user.role == 'pf_admin':
            user_ids = [u.id for u in User.query.filter_by(role='gm', location=current_user.location).all()]
            query = query.filter(ActivityLog.user_id.in_(user_ids))
        
        logs = query.order_by(ActivityLog.created_at.desc()).limit(100).all()
        
        return jsonify({
            'logs': [log.to_dict() for log in logs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PF Resource Hub API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'Planet Fitness Resource Hub API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/*',
            'users': '/api/users',
            'activity_logs': '/api/activity-logs',
            'health': '/api/health'
        }
    }), 200


# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================

def init_database():
    """Initialize database with default admin accounts"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if SES admin exists
        ses_admin = User.query.filter_by(email=Config.SES_SUPER_ADMIN_EMAIL).first()
        if not ses_admin:
            ses_admin = User(
                username='asoler',
                email=Config.SES_SUPER_ADMIN_EMAIL,
                first_name='Adriana',
                last_name='Soler',
                role='ses_admin',
                is_active=True
            )
            ses_admin.set_password('SES-Admin-2025!')  # Change this!
            db.session.add(ses_admin)
            print(f"✅ Created SES Super Admin: {ses_admin.email}")
        
        # Check if PF test admin exists
        pf_admin = User.query.filter_by(email=Config.PF_ADMIN_TEST_EMAIL).first()
        if not pf_admin:
            pf_admin = User(
                username='pfadmin',
                email=Config.PF_ADMIN_TEST_EMAIL,
                first_name='Adriana',
                last_name='Test Admin',
                role='pf_admin',
                location='Boston Region',
                is_active=True,
                created_by_id=ses_admin.id
            )
            pf_admin.set_password('PF-Admin-2025!')  # Change this!
            db.session.add(pf_admin)
            print(f"✅ Created PF Test Admin: {pf_admin.email}")
        
        db.session.commit()
        print("✅ Database initialized successfully!")


# =============================================================================
# AI CHAT ENDPOINT
# =============================================================================

@app.route('/api/chat', methods=['POST'])
@token_required
def chat(current_user):
    """
    AI Chat endpoint for HVAC troubleshooting
    Requires authentication token
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history (optional)
        conversation_history = data.get('conversation_history', [])
        
        # Get AI response
        ai_response = get_ai_response(user_message, conversation_history)
        
        # Log activity
        try:
            activity = ActivityLog(
                user_id=current_user.id,
                action='ai_chat',
                description=f"Asked AI: {user_message[:50]}..."
            )
            db.session.add(activity)
            db.session.commit()
        except:
            pass  # Don't fail if logging fails
        
        return jsonify({
            'success': True,
            'message': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500


# =============================================================================
# ANALYTICS API
# =============================================================================

@app.route('/api/analytics', methods=['GET'])
@token_required
def get_analytics(current_user):
    """Get Google Analytics data for the dashboard"""
    try:
        # Check if user is admin
        if current_user.role not in ['admin', 'ses_admin', 'pf_admin']:
            return jsonify({
                'error': 'Access denied. Admin access required.'
            }), 403
        
        # Get query parameters
        date_range = request.args.get('range', '30days')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        # Convert string dates to datetime if provided
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Fetch analytics data
        analytics_data = get_all_analytics_data(date_range, start_date, end_date)
        
        # Log activity
        try:
            activity = ActivityLog(
                user_id=current_user.id,
                action='view_analytics',
                details=f'Viewed analytics dashboard - Range: {date_range}'
            )
            db.session.add(activity)
            db.session.commit()
        except:
            pass  # Don't fail if logging fails
        
        return jsonify({
            'success': True,
            'data': analytics_data,
            'dateRange': date_range,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        print(f"❌ Analytics error: {str(e)}")
        return jsonify({
            'error': 'An error occurred while fetching analytics data',
            'details': str(e)
        }), 500


# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == '__main__':
    # Initialize database on first run
    init_database()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
