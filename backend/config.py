"""
Configuration management for SAM3 Web Application
"""
import os
from pathlib import Path

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Application configuration"""
    
    # API Keys
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    KIE_API_KEY = os.getenv("KIE_API_KEY", "")
    
    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Model settings
    DEVICE = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") != "-1" else "cpu"
    
    # kie.ai settings
    KIE_API_URL = os.getenv("KIE_API_URL", "https://api.kie.ai/v1/generate/nano-banana")
    
    # File paths
    FRONTEND_DIR = os.getenv("FRONTEND_DIR", "../frontend/dist")
    TEMP_DIR = os.getenv("TEMP_DIR", "/tmp")
    
    # Processing settings
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "100")) * 1024 * 1024  # 100MB default
    SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.5"))
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.HF_TOKEN:
            print("⚠️  Warning: HF_TOKEN not set. Model downloads may fail.")
        
        # Create temp directory if it doesn't exist
        Path(cls.TEMP_DIR).mkdir(parents=True, exist_ok=True)
        
        return True


config = Config()
