from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rooms, autocomplete, websocket
from app.database import engine, Base
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pair Programming API",
    description="Real-time collaborative coding platform",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rooms.router, prefix="/api", tags=["rooms"])
app.include_router(autocomplete.router, prefix="/api", tags=["autocomplete"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
async def root():
    return {
        "message": "Pair Programming API",
        "version": "1.0.0",
        "endpoints": {
            "create_room": "POST /api/rooms",
            "autocomplete": "POST /api/autocomplete",
            "websocket": "WS /ws/{room_id}"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
