"""Configuration de l'application"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Paramètres de configuration de l'application"""
    
    # Base de données
    database_url: str = "postgresql://user:password@localhost/petit_tonnerre"
    
    # JWT
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """Retourne les paramètres de configuration (avec cache)"""
    return Settings()
