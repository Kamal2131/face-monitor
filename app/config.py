# config.py
import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "production")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./proctor.db")
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_MIME_TYPES: list = ["image/jpeg", "image/png"]
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    CLOUDINARY_FOLDER: str = os.getenv("CLOUDINARY_FOLDER", "proctor-system")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "").split(",") or ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings() 