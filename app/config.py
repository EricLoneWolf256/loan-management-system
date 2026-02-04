# application  configuration using Pydantic Settings
# this centralises all environment variables and configuration

from pydantic_settings import BaseSettings

from typing import List

class Settings(BaseSettings):
    # the control panel for the entire application configuration
    DATABASE_URL: str
    # database connection
    
    # applicanion
    APP_NAME: str = "Loan Management System"
    PROJECT_NAME: str = "Loan Management System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str
    ALGORITHM: str = "HS256"    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in minutes
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]  # allow all origins by default
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
# GLOBAL SETTINGS INSTANCE
settings = Settings()