from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from core.config import Settings, get_settings


def new_async_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        settings.sqlalchemy_database_url,
        pool_pre_ping=settings.connection.pool_pre_ping,
        pool_size=settings.connection.pool_size,
        max_overflow=settings.connection.max_overflow,
        pool_timeout=settings.connection.pool_timeout,
        pool_recycle=settings.connection.pool_recycle,
    )

_ASYNC_ENGINE = new_async_engine(get_settings())
_ASYNC_SESSION_MAKER = async_sessionmaker(_ASYNC_ENGINE, expire_on_commit=False)

def get_async_session() -> AsyncSession:
    return _ASYNC_SESSION_MAKER()
