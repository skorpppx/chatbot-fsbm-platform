"""
Configuration centralisée du chatbot-service.
Utilise pydantic-settings pour charger depuis variables d'environnement / .env.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings du chatbot-service."""

    # Service
    service_name: str = "chatbot-service"
    service_port: int = 5001
    env: str = "development"
    debug: bool = True

    # Database
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "fsbm_db"
    db_user: str = "root"
    db_password: str = ""

    # Inter-services
    academic_service_url: str = "http://localhost:5002"

    # NLP
    confidence_threshold: float = 0.15
    max_history_messages: int = 20
    max_message_length: int = 500

    # CORS
    cors_origins: str = "http://localhost:4200,http://localhost:3000"

    # LLM
    groq_api_key: str = ""
    groq_model: str = "default"
    hf_api_key: str = ""
    rag_top_k: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",   # tolere les variables .env non declarees
    )

    @property
    def database_url(self) -> str:
        """URL SQLAlchemy async pour MySQL."""
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        """URL SQLAlchemy synchrone (pour utilitaires)."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
