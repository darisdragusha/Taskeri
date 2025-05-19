from enum import Enum
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

class EnvironmentVariable(str, Enum):
    """Enumeration of all environment variables used in the application."""

   
    DB_HOST = "DB_HOST"
    DB_NAME = "DB_NAME"
    DB_PASSWORD = "DB_PASSWORD" 
    DB_USERNAME = "DB_USERNAME"
    DB_URL = "DB_URL"
    DB_PORT = "DB_PORT"
    

    SECRET_KEY = "SECRET_KEY"
    ALGORITHM = "ALGORITHM"
    ACCESS_TOKEN_EXPIRE_MINUTES = "ACCESS_TOKEN_EXPIRE_MINUTES"
    
    HOST = "HOST"
    PORT = "PORT"

def get_env(key: EnvironmentVariable, default: str = None) -> str:
    """Get environment variable value."""
    return os.getenv(key.value, default)