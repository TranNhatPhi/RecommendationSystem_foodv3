"""
Test Real OpenAI Integration
"""

import requests
import json
import time


def test_real_openai():
    """Test if we're actually using OpenAI API"""
    base_url = "http://127.0.0.1:5000"

    print("🔍 Testing Real OpenAI Integration")
    print("=" * 50)

    # Unique test that would be hard for demo to fake
    test_data = {
        "customer_id": "1001",
        "message": "Write me a haiku about Vietnamese pho in English, then recommend a healthy breakfast",
        "location": "10.762622,106.660172"
    }

    print(f"📋 Unique Test Case (Haiku + Food Recommendation)")
    print(f"Message: {test_data['message']}")
    print("-" * 50)

    try:
        start_time = time.time()

        response = requests.post(
            f"{base_url}/api/enhanced-chat",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        end_time = time.time()
        response_time = end_time - start_time

        print(f"⏱️  Response time: {response_time:.2f}s")
        print(f"📊 Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')

            print("📝 Full Response:")
            print(response_text)
            print("-" * 50)

            # Check for signs of real OpenAI response
            if "haiku" in response_text.lower() or "pho" in response_text.lower():
                print("🎯 REAL OPENAI CONFIRMED!")
                print("✅ Contains haiku/pho content as requested")
            else:
                print("🔄 Likely Demo Response")
                print("❌ Doesn't contain haiku content")

            # Check response structure
            agent_type = data.get('agent_type', 'unknown')
            print(f"🤖 Agent Type: {agent_type}")

            if agent_type == "production":
                print("✅ Using Production Agent")
            elif agent_type == "enhanced":
                print("🔄 Using Enhanced Agent (could be demo)")
            else:
                print("❓ Unknown agent type")

        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    test_real_openai()
