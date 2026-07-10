from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file created in the current directory
DATABASE_URL = "sqlite+aiosqlite:///./osint_cache.db"

# Engine establishes connection with the database
# 'check_same_thread' must be False for asynchronous FastAPI operations
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionMaker provides permission to execute database queries
SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class to inherit from when creating database models/tables
Base = declarative_base()

# Dependency injection generator to provide database session to FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
