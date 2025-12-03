from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.room_service import RoomService
from typing import Dict, List
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Connection manager to handle multiple WebSocket connections per room
class ConnectionManager:
    def __init__(self):
        # Dictionary mapping room_id to list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        logger.info(f"Client connected to room {room_id}. Total connections: {len(self.active_connections[room_id])}")

    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove a WebSocket connection"""
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                logger.info(f"Client disconnected from room {room_id}. Remaining connections: {len(self.active_connections[room_id])}")
            
            # Clean up empty room lists
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: str, exclude: WebSocket = None):
        """Broadcast message to all connections in a room except the sender"""
        if room_id not in self.active_connections:
            return
        
        # Send to all connections except the one that sent the message
        for connection in self.active_connections[room_id]:
            if connection != exclude:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")

    def get_connection_count(self, room_id: str) -> int:
        """Get number of active connections in a room"""
        return len(self.active_connections.get(room_id, []))


manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time code collaboration
    
    Message format:
    {
        "type": "code_update" | "cursor_move" | "join" | "leave",
        "code": "...",  # for code_update
        "cursorPosition": 123,  # optional
        "userId": "user-id"  # optional
    }
    """
    # Verify room exists
    room = RoomService.get_room(db, room_id)
    if not room:
        await websocket.close(code=4004, reason="Room not found")
        return

    # Connect the WebSocket
    await manager.connect(websocket, room_id)
    
    # Increment active users
    RoomService.increment_active_users(db, room_id)
    
    # Send current room state to the newly connected client
    try:
        await websocket.send_json({
            "type": "init",
            "code": room.code,
            "language": room.language,
            "activeUsers": manager.get_connection_count(room_id)
        })
        
        # Notify other users about new connection
        await manager.broadcast({
            "type": "user_joined",
            "activeUsers": manager.get_connection_count(room_id)
        }, room_id, exclude=websocket)

    except Exception as e:
        logger.error(f"Error sending initial state: {e}")
        manager.disconnect(websocket, room_id)
        RoomService.decrement_active_users(db, room_id)
        return

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type", "code_update")
            
            if message_type == "code_update":
                # Update code in database
                code = message.get("code", "")
                RoomService.update_room_code(db, room_id, code)
                
                # Broadcast to other clients
                await manager.broadcast({
                    "type": "code_update",
                    "code": code,
                    "cursorPosition": message.get("cursorPosition"),
                    "userId": message.get("userId")
                }, room_id, exclude=websocket)
                
            elif message_type == "cursor_move":
                # Broadcast cursor position to other clients
                await manager.broadcast({
                    "type": "cursor_move",
                    "cursorPosition": message.get("cursorPosition"),
                    "userId": message.get("userId")
                }, room_id, exclude=websocket)
                
            elif message_type == "ping":
                # Respond to ping to keep connection alive
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for room {room_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Clean up on disconnect
        manager.disconnect(websocket, room_id)
        RoomService.decrement_active_users(db, room_id)
        
        # Notify remaining users
        await manager.broadcast({
            "type": "user_left",
            "activeUsers": manager.get_connection_count(room_id)
        }, room_id)
