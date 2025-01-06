# repast/config.py
from functools import lru_cache
import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()  # Load .env file
        
        # Required settings (will raise error if not set)
        self.API_KEY = self._get_required('API_KEY')
        self.GOOGLE_PLACES_API_KEY = self._get_required('GOOGLE_PLACES_API_KEY')
        self.GOOGLE_AI_API_KEY = self._get_required('GOOGLE_AI_API_KEY')
        
        # Optional settings with defaults
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'development')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        
    def _get_required(self, name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise ValueError(f"Missing required environment variable: {name}")
        return value

@lru_cache()
def get_settings() -> Settings:
    return Settings()