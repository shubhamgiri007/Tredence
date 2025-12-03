"""
Simple test script to verify the API endpoints
Run after starting the server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_create_room():
    """Test room creation"""
    response = requests.post(f"{BASE_URL}/api/rooms", json={"language": "python"})
    print(f"Create Room: {response.status_code}")
    data = response.json()
    print(f"Response: {data}\n")
    return data.get("roomId")

def test_get_room(room_id):
    """Test getting room details"""
    response = requests.get(f"{BASE_URL}/api/rooms/{room_id}")
    print(f"Get Room: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_autocomplete():
    """Test autocomplete endpoint"""
    payload = {
        "code": "def hello",
        "cursorPosition": 9,
        "language": "python"
    }
    response = requests.post(f"{BASE_URL}/api/autocomplete", json=payload)
    print(f"Autocomplete: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("=== Testing Pair Programming API ===\n")
    
    try:
        test_health()
        room_id = test_create_room()
        if room_id:
            test_get_room(room_id)
        test_autocomplete()
        
        print("All tests completed!")
    except Exception as e:
        print(f"Error: {e}")
