from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.room_service import RoomService
from app.schemas.room import RoomCreate, RoomResponse

router = APIRouter()


@router.post("/rooms", response_model=RoomResponse, status_code=201)
async def create_room(
    room_data: RoomCreate = RoomCreate(),
    db: Session = Depends(get_db)
):
    """
    Create a new room for pair programming
    
    Returns:
        RoomResponse with roomId and initial state
    """
    room = RoomService.create_room(db, language=room_data.language)
    return RoomResponse(
        roomId=room.id,
        code=room.code,
        language=room.language,
        created_at=room.created_at,
        active_users=room.active_users
    )


@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Get room details by room ID
    
    Args:
        room_id: The room identifier
        
    Returns:
        RoomResponse with room details
    """
    room = RoomService.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return RoomResponse(
        roomId=room.id,
        code=room.code,
        language=room.language,
        created_at=room.created_at,
        active_users=room.active_users
    )
