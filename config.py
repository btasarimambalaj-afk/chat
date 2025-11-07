import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    
    # Admin
    ADMIN_OTP_VALIDITY_MINUTES = int(os.getenv('ADMIN_OTP_VALIDITY_MINUTES', 5))
    ADMIN_SESSION_HOURS = int(os.getenv('ADMIN_SESSION_HOURS', 10))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=int(os.getenv('ADMIN_SESSION_HOURS', 10)))
    
    # File Upload
    MAX_IMAGE_SIZE_MB = int(os.getenv('MAX_IMAGE_SIZE_MB', 5))
    MAX_VOICE_SIZE_MB = int(os.getenv('MAX_VOICE_SIZE_MB', 10))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    
    UPLOAD_FOLDER = 'static/uploads'
    IMAGE_UPLOAD_FOLDER = 'static/uploads/images'
    VOICE_UPLOAD_FOLDER = 'static/uploads/voices'
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    ALLOWED_VOICE_EXTENSIONS = {'webm', 'ogg', 'mp3', 'wav', 'm4a'}
    
    # Database
    DATABASE_PATH = 'database.db'
    
    # Rate Limiting
    RATE_LIMIT_MESSAGES = 20  # per minute
    RATE_LIMIT_UPLOADS = 5    # per minute
    RATE_LIMIT_OTP = 3        # per 5 minutes
