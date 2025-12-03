# Real-Time Pair Programming Platform

A full-stack collaborative coding application that enables real-time pair programming with AI-powered autocomplete suggestions.

##  Features

- **Real-time Collaboration**: Multiple users can code together in the same room with instant synchronization
- **WebSocket Communication**: Low-latency updates using WebSocket connections
- **AI Autocomplete**: Mocked intelligent code suggestions based on context
- **Room Management**: Create and join coding rooms with unique identifiers
- **Persistent Storage**: PostgreSQL database for room state management
- **Clean Architecture**: Well-structured backend with separation of concerns

##  Architecture

### Backend Structure
```
backend/
 app/
    __init__.py
    main.py              # Application entry point
    config.py            # Configuration management
    database.py          # Database setup
    models/              # SQLAlchemy models
       __init__.py
       room.py
    schemas/             # Pydantic schemas
       __init__.py
       room.py
       autocomplete.py
    routers/             # API endpoints
       __init__.py
       rooms.py
       autocomplete.py
       websocket.py
    services/            # Business logic
        __init__.py
        room_service.py
        autocomplete_service.py
 scripts/
    init_db.py           # Database initialization
 tests/
    test_api.py          # REST API tests
    test_websocket.py    # WebSocket tests
 requirements.txt
 .env.example
 run.py
```

##  Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/shubhamgiri007/Tredence.git
cd Tredence/backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL**

Create a PostgreSQL database:
```sql
CREATE DATABASE pairprogramming;
```

5. **Configure environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and update DATABASE_URL
# DATABASE_URL=postgresql://username:password@localhost:5432/pairprogramming
```

6. **Initialize database**
```bash
python scripts/init_db.py
```

7. **Run the application**
```bash
# Using run.py
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation (Swagger): `http://localhost:8000/docs`

##  API Endpoints

### REST API

#### 1. Health Check
```http
GET /health
```
Returns API health status.

#### 2. Create Room
```http
POST /api/rooms
Content-Type: application/json

{
  "language": "python"  // optional, defaults to "python"
}
```
**Response:**
```json
{
  "roomId": "uuid-string",
  "code": "# Start coding here...\n",
  "language": "python",
  "created_at": "2025-12-03T10:00:00",
  "active_users": 0
}
```

#### 3. Get Room Details
```http
GET /api/rooms/{room_id}
```
**Response:**
```json
{
  "roomId": "uuid-string",
  "code": "current code content",
  "language": "python",
  "created_at": "2025-12-03T10:00:00",
  "active_users": 2
}
```

#### 4. Autocomplete Suggestion
```http
POST /api/autocomplete
Content-Type: application/json

{
  "code": "def hello",
  "cursorPosition": 9,
  "language": "python"
}
```
**Response:**
```json
{
  "suggestion": "def function_name(param1, param2):\n    pass",
  "confidence": 0.85,
  "type": "snippet"
}
```

### WebSocket API

#### Connect to Room
```
WS /ws/{room_id}
```

**Server → Client Messages:**

1. **Initial State**
```json
{
  "type": "init",
  "code": "current code",
  "language": "python",
  "activeUsers": 1
}
```

2. **Code Update**
```json
{
  "type": "code_update",
  "code": "updated code",
  "cursorPosition": 123,
  "userId": "user-id"
}
```

3. **User Joined**
```json
{
  "type": "user_joined",
  "activeUsers": 2
}
```

4. **User Left**
```json
{
  "type": "user_left",
  "activeUsers": 1
}
```

**Client → Server Messages:**

1. **Code Update**
```json
{
  "type": "code_update",
  "code": "new code content",
  "cursorPosition": 123,
  "userId": "optional-user-id"
}
```

2. **Cursor Move**
```json
{
  "type": "cursor_move",
  "cursorPosition": 123,
  "userId": "optional-user-id"
}
```

3. **Keep-Alive**
```json
{
  "type": "ping"
}
```

##  Testing

### Test REST API
```bash
# Install requests library if not already installed
pip install requests

# Run tests
python tests/test_api.py
```

### Test WebSocket
```bash
# Install websockets library if not already installed
pip install websockets

# Run tests
python tests/test_websocket.py
```

### Manual Testing with curl

**Create a room:**
```bash
curl -X POST http://localhost:8000/api/rooms \
  -H "Content-Type: application/json" \
  -d '{"language": "python"}'
```

**Get autocomplete:**
```bash
curl -X POST http://localhost:8000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello", "cursorPosition": 9, "language": "python"}'
```

### Testing with Postman

1. Import the endpoints into Postman
2. Create a room using POST request
3. Use the WebSocket feature in Postman to connect to `ws://localhost:8000/ws/{room_id}`
4. Send JSON messages to test real-time updates

##  Design Choices

### 1. **Architecture Pattern**
- **Layered Architecture**: Separation of concerns with routers, services, and models
- **Dependency Injection**: Using FastAPI's dependency system for database sessions
- **Service Layer**: Business logic isolated from API endpoints

### 2. **Database Design**
- **PostgreSQL**: Reliable, ACID-compliant relational database
- **SQLAlchemy ORM**: Type-safe database operations with migrations support
- **Simple Schema**: Single `rooms` table with code state and metadata

### 3. **Real-Time Communication**
- **WebSockets**: Full-duplex communication for instant updates
- **Connection Manager**: Centralized WebSocket connection handling
- **Room-based Broadcasting**: Messages only sent to users in the same room
- **Last-Write Wins**: Simple conflict resolution strategy

### 4. **Autocomplete System**
- **Pattern Matching**: Regex-based code pattern recognition
- **Context-Aware**: Analyzes current line and code structure
- **Extensible**: Easy to add new patterns or integrate real AI models
- **Language Support**: Configurable for different programming languages

### 5. **Code Organization**
- **Modular Structure**: Clear separation of routes, services, models
- **Type Safety**: Pydantic schemas for request/response validation
- **Configuration Management**: Environment-based settings with .env support

##  Configuration

Environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# CORS - Add your frontend URLs
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Debug mode
DEBUG=True
```

##  Limitations & Known Issues

1. **Conflict Resolution**: Uses last-write-wins strategy. No operational transformation (OT) or CRDT.
2. **Scalability**: In-memory connection manager. For production, use Redis pub/sub.
3. **Authentication**: No user authentication or authorization implemented.
4. **Room Persistence**: Rooms are never deleted automatically.
5. **Code History**: No version control or undo/redo functionality.
6. **File Upload**: No support for multiple files or file upload.
7. **AI Autocomplete**: Mock implementation with pattern matching, not real AI.
8. **Rate Limiting**: No rate limiting on API endpoints or WebSocket messages.
9. **Database Migrations**: No migration system (Alembic) configured.
10. **Testing**: Limited test coverage, no unit tests for services.

##  Future Improvements

### With More Time (Priority Order)

1. **Operational Transformation (OT)**
   - Implement proper conflict resolution for simultaneous edits
   - Handle cursor position updates during concurrent changes
   - Use libraries like ShareDB or custom OT implementation

2. **Real AI Integration**
   - Integrate with OpenAI Codex or GitHub Copilot API
   - Local model using CodeGen or StarCoder
   - Context-aware suggestions based on entire codebase

3. **Enhanced Scalability**
   - Redis for pub/sub and session storage
   - Horizontal scaling with multiple server instances
   - Load balancer configuration

4. **Authentication & Authorization**
   - User registration and login (JWT tokens)
   - Room ownership and permissions
   - Private/public room settings

5. **Advanced Features**
   - Multiple file support
   - Syntax highlighting backend support
   - Code execution in sandboxed environment
   - Video/audio chat integration
   - Real-time cursor positions with user avatars

6. **Code Quality**
   - Comprehensive unit and integration tests
   - CI/CD pipeline setup
   - Code coverage reporting
   - Database migration system (Alembic)

7. **Frontend Development**
   - React + TypeScript frontend
   - Monaco Editor or CodeMirror integration
   - Redux Toolkit for state management
   - Real-time cursor indicators

8. **Monitoring & Observability**
   - Logging with structured logs
   - Metrics collection (Prometheus)
   - Error tracking (Sentry)
   - Performance monitoring

9. **Security Enhancements**
   - Rate limiting
   - Input sanitization
   - XSS/CSRF protection
   - Secure WebSocket connections (WSS)

10. **User Experience**
    - Room expiration and cleanup
    - Code templates
    - Keyboard shortcuts
    - Mobile responsive design

##  Database Schema

```sql
CREATE TABLE rooms (
    id VARCHAR PRIMARY KEY,
    code TEXT DEFAULT '# Start coding here...\n',
    language VARCHAR DEFAULT 'python',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    active_users INTEGER DEFAULT 0
);
```

##  Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution**: Kill the process using port 8000 or change the port in `run.py`.

### WebSocket Connection Failed
**Solution**: Ensure CORS settings allow your frontend origin in `.env`.

##  License

This project is created for demonstration purposes.

##  Author

Tredence Full-Stack Python API Developer Assignment

##  Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- WebSocket protocol specification
