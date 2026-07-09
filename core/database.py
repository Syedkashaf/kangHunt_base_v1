from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file ka naam jo hamare folder mein banegi
DATABASE_URL = "sqlite+aiosqlite:///./osint_cache.db"

# Engine database ke sath connection establish karta hai
# 'check_same_thread' False karna zaroori hai asynchronous FastAPI ke liye
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionMaker humein database queries execute karne ki permission deta hai
SessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class jisko inherit kar ke hum apne tables banayenge
Base = declarative_base()

# Dependency injection generator (FastAPI ko database session dene ke liye)
async def get_db():
    async with SessionLocal() as session:
        yield session
