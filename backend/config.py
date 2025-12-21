# Configuration for Planet Fitness Resource Hub Backend
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///pf_resource_hub.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
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
