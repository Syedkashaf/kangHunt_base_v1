"""
Central configuration management for kangHunt_base_v1
Integrates both kangHunt and GHunt configurations
"""

import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()


class Config:
    """Base configuration class"""
    
    # Application settings
    APP_NAME = "kangHunt_base_v1"
    APP_VERSION = "1.1.0"
    APP_DESCRIPTION = "Advanced Modular OSINT Framework with integrated GHunt v2.3.4"
    
    # Environment
    ENV = os.getenv("ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security & API
    CORE_API_KEY = os.getenv("CORE_API_KEY", "change-me-in-production")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))
    
    # GHunt Configuration
    GHUNT_VERSION = "2.3.4"
    GHUNT_ENABLED = os.getenv("GHUNT_ENABLED", "True").lower() == "true"
    GHUNT_CREDS_PATH = os.getenv("GHUNT_CREDS_PATH", ".ghunt_creds")
    GHUNT_CACHE_DIR = os.getenv("GHUNT_CACHE_DIR", ".ghunt_cache")
    
    # Google OAuth Settings (for GHunt)
    GOOGLE_OAUTH_TOKEN = os.getenv("GOOGLE_OAUTH_TOKEN", "")
    GOOGLE_MASTER_TOKEN = os.getenv("GOOGLE_MASTER_TOKEN", "")
    GOOGLE_COOKIES = os.getenv("GOOGLE_COOKIES", "")
    
    # Gravatar Configuration
    GRAVATAR_ENABLED = os.getenv("GRAVATAR_ENABLED", "True").lower() == "true"
    
    # Holehe Configuration
    HOLEHE_ENABLED = os.getenv("HOLEHE_ENABLED", "True").lower() == "true"
    
    # XposedOrNot Configuration
    XPOSED_ENABLED = os.getenv("XPOSED_ENABLED", "True").lower() == "true"
    
    # IntelBase Configuration
    INTELBASE_ENABLED = os.getenv("INTELBASE_ENABLED", "True").lower() == "true"
    INTELBASE_API_KEY = os.getenv("INTELBASE_API_KEY", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "kangHunt.log")
    
    # Performance
    WORKERS = int(os.getenv("WORKERS", "4"))
    ASYNC_WORKERS = int(os.getenv("ASYNC_WORKERS", "10"))
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
    
    # Output
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")  # json, html, csv, txt
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./results")
    
    @staticmethod
    def get_ghunt_config() -> Dict[str, Any]:
        """Get GHunt-specific configuration"""
        return {
            "enabled": Config.GHUNT_ENABLED,
            "version": Config.GHUNT_VERSION,
            "creds_path": Config.GHUNT_CREDS_PATH,
            "cache_dir": Config.GHUNT_CACHE_DIR,
            "oauth_token": Config.GOOGLE_OAUTH_TOKEN,
            "master_token": Config.GOOGLE_MASTER_TOKEN,
            "cookies": Config.GOOGLE_COOKIES,
        }
    
    @staticmethod
    def get_osint_sources() -> Dict[str, bool]:
        """Get enabled OSINT sources"""
        return {
            "ghunt": Config.GHUNT_ENABLED,
            "gravatar": Config.GRAVATAR_ENABLED,
            "holehe": Config.HOLEHE_ENABLED,
            "xposed": Config.XPOSED_ENABLED,
            "intelbase": Config.INTELBASE_ENABLED,
        }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = "development"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = "production"
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    ENV = "testing"
    LOG_LEVEL = "DEBUG"
    GHUNT_ENABLED = False
    GRAVATAR_ENABLED = False
    HOLEHE_ENABLED = False
    XPOSED_ENABLED = False
    INTELBASE_ENABLED = False


def get_config() -> Config:
    """Get appropriate configuration based on environment"""
    env = os.getenv("ENV", "production").lower()
    
    if env == "development":
        return DevelopmentConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return ProductionConfig()


# Export active config
config = get_config()
