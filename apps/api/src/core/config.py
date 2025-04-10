from functools import lru_cache
from pathlib import Path
from sys import maxsize
from pydantic import AnyHttpUrl, BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL

PROJECT_DIR = Path(__file__).parent.parent.parent.parent.parent

class Security(BaseModel):
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    backend_cors_origins: list[AnyHttpUrl] = []

class Database(BaseModel):
    hostname: str = "postgres"
    username: str = "postgres"
    password: SecretStr
    port: int = 5432
    database: str = "postgres"

class Connection(BaseModel):
    pool_pre_ping: bool = True
    pool_size: int = 100
    max_overflow: int = 100
    pool_timeout: float = 30.0
    pool_recycle: int = 60

class Settings(BaseSettings):
    database: Database
    security: Security
    connection: Connection

    @computed_field
    @property
    def sqlalchemy_database_url(self) -> URL:
        return URL.create(
            drivername="postgres+asyncpg",
            username=self.database.username,
            password=self.database.password.get_secret_value(),
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.database,
        )

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
