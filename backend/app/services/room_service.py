from sqlalchemy.orm import Session
from app.models.room import Room
from typing import Optional
import uuid


class RoomService:
    """Service for managing rooms and code state"""

    @staticmethod
    def create_room(db: Session, language: str = "python") -> Room:
        """Create a new room"""
        room = Room(
            id=str(uuid.uuid4()),
            language=language,
            code="
            active_users=0
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    @staticmethod
    def get_room(db: Session, room_id: str) -> Optional[Room]:
        """Get room by ID"""
        return db.query(Room).filter(Room.id == room_id).first()

    @staticmethod
    def update_room_code(db: Session, room_id: str, code: str) -> Optional[Room]:
        """Update room code"""
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            room.code = code
            db.commit()
            db.refresh(room)
        return room

    @staticmethod
    def increment_active_users(db: Session, room_id: str) -> Optional[Room]:
        """Increment active users count"""
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            room.active_users = (room.active_users or 0) + 1
            db.commit()
            db.refresh(room)
        return room

    @staticmethod
    def decrement_active_users(db: Session, room_id: str) -> Optional[Room]:
        """Decrement active users count"""
        room = db.query(Room).filter(Room.id == room_id).first()
        if room:
            room.active_users = max(0, (room.active_users or 0) - 1)
            db.commit()
            db.refresh(room)
        return room
