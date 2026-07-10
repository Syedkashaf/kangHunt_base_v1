from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL for local caching
DATABASE_URL = "sqlite+aiosqlite:///./osint_cache.db"

# Create async database engine with thread safety disabled for FastAPI
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Factory for creating async database sessions
SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for SQLAlchemy ORM models
Base = declarative_base()

# Dependency injection function for database sessions in FastAPI routes
async def get_db():
    """Yields a database session for use in API endpoints."""
    async with SessionLocal() as session:
        yield session
