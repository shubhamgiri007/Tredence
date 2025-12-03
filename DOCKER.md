# Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker Desktop for Windows
- Docker Compose

### Steps

1. **Start the services**
```powershell
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Build and start the FastAPI backend
- Initialize the database automatically

2. **Check status**
```powershell
docker-compose ps
```

3. **View logs**
```powershell
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Database only
docker-compose logs -f postgres
```

4. **Access the application**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

5. **Stop the services**
```powershell
docker-compose down
```

6. **Stop and remove volumes (clean slate)**
```powershell
docker-compose down -v
```

## Manual Docker Commands

### Build backend image
```powershell
cd backend
docker build -t pair-programming-backend .
```

### Run PostgreSQL
```powershell
docker run -d `
  --name postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=pairprogramming `
  -p 5432:5432 `
  postgres:15-alpine
```

### Run backend
```powershell
docker run -d `
  --name backend `
  -p 8000:8000 `
  -e DATABASE_URL=postgresql://postgres:postgres@postgres:5432/pairprogramming `
  --link postgres:postgres `
  pair-programming-backend
```

## Database Access

### Connect to PostgreSQL in Docker
```powershell
docker exec -it postgres psql -U postgres -d pairprogramming
```

### Initialize database manually
```powershell
docker-compose exec backend python scripts/init_db.py
```

## Troubleshooting

### Backend can't connect to database
```powershell
# Check if postgres is healthy
docker-compose ps

# Restart services
docker-compose restart
```

### Port conflicts
```powershell
# Stop conflicting services
docker-compose down

# Or change ports in docker-compose.yml
```

### Reset everything
```powershell
docker-compose down -v
docker-compose up -d --build
```
