from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RoomCreate(BaseModel):
    language: str = Field(default="python", description="Programming language")


class RoomResponse(BaseModel):
    roomId: str
    code: Optional[str] = None
    language: Optional[str] = None
    created_at: Optional[datetime] = None
    active_users: Optional[int] = 0

    class Config:
        from_attributes = True


class CodeUpdate(BaseModel):
    code: str
    cursorPosition: Optional[int] = None
    userId: Optional[str] = None
