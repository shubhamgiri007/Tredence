# System Architecture

## Overview

The Pair Programming Platform is built with a layered architecture separating concerns between data, business logic, and presentation layers.

## Architecture Diagram

```

                         CLIENTS                              
            
     Browser         Postman        Python Test       
    (demo.html)                      Scripts          
            

                                              
           HTTP/WS           HTTP/WS           HTTP/WS
                                              

                    FASTAPI APPLICATION                       
     
                   MIDDLEWARE LAYER                         
                
        CORS        Logging        Error            
     Middleware    Middleware     Handler           
                
     
                                                             
     
                     ROUTER LAYER                           
              
      Rooms      Autocomplete     WebSocket         
      Router        Router          Router          
     /api/rooms  /api/autocomplete /ws/{id}          
              
     
                                                           
     
                    SERVICE LAYER                           
             
     RoomService     AutocompleteService               
                                                       
     - create()      - get_suggestion()                
     - get()         - pattern_matching()              
     - update()      - context_analysis()              
             
     
                                                              
     
                  CONNECTION MANAGER                          
            
      WebSocket Connection Pool                            
      {room_id: [ws1, ws2, ws3, ...]}                     
                                                           
      - connect(ws, room_id)                              
      - disconnect(ws, room_id)                           
      - broadcast(msg, room_id, exclude)                  
            
     
                                                              
     
                     DATA LAYER                               
                   
      SQLAlchemy      Pydantic Schemas          
        Models                                           
                            - RoomCreate                 
      - Room                - RoomResponse               
        - id                - AutocompleteRequest        
        - code              - AutocompleteResponse       
        - language               
                                             
     

             

                    DATABASE LAYER                            
    
                PostgreSQL Database                          
                                                             
         
      Table: rooms                                        
            
       id (PK)       VARCHAR   UUID                  
       code          TEXT      Code content          
       language      VARCHAR   python/js/etc         
       created_at    TIMESTAMP Creation time         
       updated_at    TIMESTAMP Last update           
       active_users  INTEGER   User count            
            
         
    

```

## Communication Flow

### REST API Flow (Room Creation)
```
Client                Router              Service           Database
                                                           
  POST /api/rooms                                    
                       create_room()                 
                                          INSERT INTO
                                          room
                       room_data                 
  RoomResponse                                    
     {roomId}                                              
```

### WebSocket Flow (Real-time Collaboration)
```
User 1              WebSocket Router    ConnectionManager    Database
                                                             
  WS /ws/{room_id}                                    
                         connect(ws)                
                                             add to pool
  init message                                    
     {code, language}                                        
                                                             
  code_update                                    
     {code: "..."}       update_code()                
                                             UPDATE
                         broadcast()                
                           (to User 2)                       
  
User 2                                                        
  code_update                                    
     {code: "..."}                                           
```

### Autocomplete Flow
```
Client              Router              Service
                                        
  POST /autocomplete                   
    {code, cursor}                      
                     get_suggestion()
                                        analyze_code()
                                        pattern_match()
                                        generate_suggestion()
                     suggestion
  response                   
    {suggestion,                        
     confidence}                        
```

## Component Details

### 1. FastAPI Application
- **Main App**: Entry point, middleware configuration
- **CORS**: Allow cross-origin requests from frontend
- **Auto Documentation**: Swagger UI at /docs

### 2. Router Layer
- **Rooms Router**: Handle room creation and retrieval
- **Autocomplete Router**: Process autocomplete requests
- **WebSocket Router**: Manage real-time connections

### 3. Service Layer
- **RoomService**: Business logic for room operations
- **AutocompleteService**: Pattern matching and suggestion generation
- **Separation of Concerns**: Keep routers thin, logic in services

### 4. Connection Manager
- **In-Memory Storage**: Dictionary of room_id → WebSocket list
- **Broadcast Logic**: Send updates to all except sender
- **Connection Lifecycle**: Handle connect/disconnect events

### 5. Data Layer
- **SQLAlchemy Models**: ORM for database operations
- **Pydantic Schemas**: Request/response validation
- **Type Safety**: Catch errors at development time

### 6. Database
- **PostgreSQL**: Reliable, ACID-compliant storage
- **Simple Schema**: Single table for MVP
- **Extensible**: Easy to add features (users, history, etc.)

## Data Flow Patterns

### Synchronous (REST API)
1. Client sends HTTP request
2. Router validates input (Pydantic)
3. Service processes business logic
4. Database operation (if needed)
5. Response returned to client

### Asynchronous (WebSocket)
1. Client establishes WebSocket connection
2. ConnectionManager tracks active connections
3. Client sends message via WebSocket
4. Server processes and updates database
5. Server broadcasts to other clients in room
6. All clients receive update simultaneously

## Scalability Considerations

### Current Architecture (MVP)
- Single server instance
- In-memory connection management
- Direct database connections

### Production Architecture (Future)
```
Load Balancer
     
     
                    
   API   API   API   API  (Multiple instances)
                    
     
           
    
                 
  Redis      PostgreSQL
  (Pub/Sub)  (Persistence)
```

### Improvements for Scale
1. **Redis Pub/Sub**: Replace in-memory ConnectionManager
2. **Load Balancing**: Multiple API instances
3. **Session Stickiness**: Or stateless with Redis
4. **Database Pooling**: Connection pool optimization
5. **Caching**: Redis for frequently accessed rooms

## Security Considerations

### Current Implementation
- No authentication (as per requirements)
- CORS enabled for specific origins
- Input validation via Pydantic

### Production Requirements
- JWT authentication
- Rate limiting
- Input sanitization
- WebSocket authentication
- HTTPS/WSS only
- SQL injection prevention (ORM helps)

## Technology Choices Rationale

### Why FastAPI?
- Native async/await support
- Automatic API documentation
- Type hints and validation
- WebSocket support
- High performance

### Why PostgreSQL?
- ACID compliance
- JSON support (future flexibility)
- Reliable and battle-tested
- Good Python ecosystem support

### Why SQLAlchemy?
- Mature ORM
- Type-safe queries
- Migration support (Alembic)
- Prevents SQL injection

### Why In-Memory ConnectionManager?
- Simple for MVP
- Low latency
- No external dependencies
- Easy to understand and debug
