import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY               = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI  = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY           = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    UPLOAD_FOLDER            = 'uploads'
    MAX_CONTENT_LENGTH       = 16 * 1024 * 1024  

    # CORS vuln config
    CORS_ORIGINS             = "*"
    CORS_METHODS             = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS       = "*"
    CORS_EXPOSE_HEADERS      = ["Content-Type", "Authorization", "X-Custom-Header"]
    CORS_SUPPORTS_CREDENTIALS = True 


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
}