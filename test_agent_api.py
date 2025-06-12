import requests
import json


def test_ai_agent():
    """Test the AI agent API"""
    url = "http://localhost:5000/api/agent_chat"

    test_data = {
        "message": "Tôi muốn ăn món gì tốt cho sức khỏe?",
        "user_id": "CUS00001",
        "location": "Hà Nội"
    }

    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(
            f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {str(e)}")


def test_agent_stats():
    """Test the agent stats API"""
    url = "http://localhost:5000/api/agent_stats"

    try:
        response = requests.get(url)
        print(f"Stats - Status Code: {response.status_code}")
        print(
            f"Stats - Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    print("🧪 Testing AI Agent APIs...")
    print("\n1. Testing Agent Chat:")
    test_ai_agent()

    print("\n2. Testing Agent Stats:")
    test_agent_stats()
