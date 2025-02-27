import os
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    mode: str
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    db_pool_size: int = 50
    db_max_overflow: int = 10
    convention: dict[str, Any] = {
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()]
        ),
        "ix": "ix__%(table_name)s__%(all_column_names)s",
        "uq": "uq__%(table_name)s__%(all_column_names)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s",
    }

    debug: int = 1

    jwt_secret_key: str = "B0IlAowlGMfz3QoOHIlMOkmWnFWjDfjI7brDKwqhF8U"
    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24 * 7

    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=os.path.join(BASE_DIR, ".env")
    )

    @property
    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
