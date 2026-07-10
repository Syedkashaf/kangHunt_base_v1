from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite+aiosqlite:///./osint_cache.db"

# Async database engine (check_same_thread=False for FastAPI)
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Async session factory
SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# ORM base class for models
Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with SessionLocal() as session:
        yield session
