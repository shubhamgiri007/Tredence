"""
WebSocket client test
Tests real-time collaboration features
"""
import asyncio
import websockets
import json

async def test_websocket():
    """Test WebSocket connection and messaging"""

    import requests
    response = requests.post("http://localhost:8000/api/rooms", json={"language": "python"})
    room_id = response.json()["roomId"]
    print(f"Created room: {room_id}\n")

    uri = f"ws://localhost:8000/ws/{room_id}"

    async with websockets.connect(uri) as websocket:
        init_msg = await websocket.recv()
        print(f"Received init: {init_msg}\n")

        code_update = {
            "type": "code_update",
            "code": "def hello_world():\n    print('Hello, World!')",
            "userId": "test-user-1"
        }
        await websocket.send(json.dumps(code_update))
        print(f"Sent code update\n")

        cursor_update = {
            "type": "cursor_move",
            "cursorPosition": 25,
            "userId": "test-user-1"
        }
        await websocket.send(json.dumps(cursor_update))
        print(f"Sent cursor update\n")

        await asyncio.sleep(2)

        print("WebSocket test completed!")

if __name__ == "__main__":
    asyncio.run(test_websocket())
