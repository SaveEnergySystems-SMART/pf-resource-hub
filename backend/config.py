# Configuration for Planet Fitness Resource Hub Backend
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database - Force PostgreSQL, no SQLite fallback
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # If DATABASE_URL is not set, raise an error instead of falling back to SQLite
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required!")
    
    # Fix for postgres:// vs postgresql:// URL scheme
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Debug logging - print database connection info
    print(f"🔍 DATABASE_URL from environment: {DATABASE_URL[:50]}...")
    print(f"🔍 Database type: {'PostgreSQL' if 'postgresql://' in DATABASE_URL else 'SQLite' if 'sqlite:///' in DATABASE_URL else 'Unknown'}")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # SendGrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
    SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@saveenergysystems.com')
    SENDGRID_FROM_NAME = os.environ.get('SENDGRID_FROM_NAME', 'Save Energy Systems')
    
    # Frontend URL
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://pf-resource-hub.pages.dev')
    
    # Admin Emails (from user requirements)
    SES_SUPER_ADMIN_EMAIL = 'asoler@saveenergysystems.com'
    PF_ADMIN_TEST_EMAIL = 'adrianasolercreative@gmail.com'
    
    # Email Mode
    EMAIL_MODE = os.environ.get('EMAIL_MODE', 'console')  # 'console' or 'sendgrid'
    
    # CORS
    CORS_ORIGINS = [
        'https://pf-resource-hub.pages.dev',
        'https://*.pf-resource-hub.pages.dev',  # All Cloudflare preview branches
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://*.sandbox.novita.ai'  # All sandbox URLs
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
