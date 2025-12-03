# Quick Start Guide

## 1. PostgreSQL Setup (Windows)

### Install PostgreSQL
1. Download from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user
4. Default port is 5432

### Create Database
1. Open pgAdmin 4 (installed with PostgreSQL)
2. Connect to the server
3. Right-click "Databases" → Create → Database
4. Name: `pairprogramming`
5. Click "Save"

**OR use command line:**
```powershell
# Open PowerShell as Administrator
psql -U postgres

# In psql prompt
CREATE DATABASE pairprogramming;
\q
```

## 2. Backend Setup

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item .env.example .env

# Edit .env file with your database credentials
notepad .env

# Update this line in .env:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/pairprogramming

# Initialize database
python scripts\init_db.py

# Run the server
python run.py
```

## 3. Verify Installation

Open your browser and visit:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 4. Test the API

### Using Python
```powershell
# Run the test script
python tests\test_api.py
```

### Using Browser (Swagger UI)
1. Go to http://localhost:8000/docs
2. Click on "POST /api/rooms" → "Try it out" → "Execute"
3. Copy the `roomId` from the response
4. Test "POST /api/autocomplete" with sample code

## 5. Test WebSocket

### Using Python
```powershell
# Install websockets if needed
pip install websockets

# Run WebSocket test
python tests\test_websocket.py
```

### Using Browser Console
```javascript
// Create a room first via API, then use the roomId
const ws = new WebSocket('ws://localhost:8000/ws/YOUR_ROOM_ID');

ws.onmessage = (event) => {
    console.log('Received:', JSON.parse(event.data));
};

ws.onopen = () => {
    console.log('Connected!');
    // Send code update
    ws.send(JSON.stringify({
        type: 'code_update',
        code: 'def hello():\n    print("Hello")',
        userId: 'test-user'
    }));
};
```

## Troubleshooting

### PostgreSQL not running
```powershell
# Check if PostgreSQL service is running
Get-Service -Name postgresql*

# Start the service
Start-Service postgresql-x64-14  # Replace with your version
```

### Database connection fails
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database `pairprogramming` exists
- Test connection: `psql -U postgres -d pairprogramming`

### Import errors
```powershell
# Make sure you're in the backend directory
cd backend

# Reinstall requirements
pip install -r requirements.txt
```

### Port 8000 already in use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (use PID from above)
taskkill /PID <PID> /F

# Or change port in run.py to 8001
```

## Next Steps

1. Create a room: `POST /api/rooms`
2. Open two browser windows
3. Connect both to the same room via WebSocket
4. Type in one window, see updates in the other
5. Test autocomplete with different code patterns
