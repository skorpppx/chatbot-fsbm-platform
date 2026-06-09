"""Configuration centralisée du academic-service."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "academic-service"
    service_port: int = 5002
    env: str = "development"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "fsbm_db"
    db_user: str = "root"
    db_password: str = ""

    cors_origins: str = "http://localhost:4200,http://localhost:5001"

    # ─── AUTH JWT (PHASE 2) ───────────────────────────────────────────────────
    jwt_secret: str = "CHANGE_ME_fsbm_super_secret_key_2026_pfe"  # override via .env
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 720          # 12 h
    # Modération des avis : True = visibles immédiatement (post-modération)
    reviews_auto_approve: bool = True

    # ─── UPLOADS (PHASE 2) ────────────────────────────────────────────────────
    upload_dir: str = "uploads"            # dossier local de stockage
    public_base_url: str = "http://localhost:8002"   # base des URLs servies
    max_upload_mb: int = 8                 # taille max d'un fichier

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",   # tolere les variables .env non declarees
    )

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
