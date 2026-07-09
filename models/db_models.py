from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from core.database import Base

class OSINTCache(Base):
    __tablename__ = "osint_query_cache"

    id = Column(Integer, primary_key=True, index=True)
    # Target (jaise email) index hoga taake search lightning fast ho
    target_query = Column(String, index=True, nullable=False)
    # Pura JSON result string mein save hoga
    raw_response = Column(Text, nullable=False)
    # Timestamp taake hum purana cache delete kar sakein
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
