from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(Text, default="")
    language = Column(String, default="python")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    active_users = Column(Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "language": self.language,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "active_users": self.active_users
        }
