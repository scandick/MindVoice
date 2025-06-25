"""Database connection and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import settings


Base = declarative_base()

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Session maker for dependency injection
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Yield an asynchronous session."""
    async with AsyncSessionLocal() as session:
        yield session
