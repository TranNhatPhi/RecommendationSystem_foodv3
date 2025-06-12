"""
Test Production Enhanced Agent API
"""

import requests
import json
import time


def test_production_api():
    """Test the production enhanced API"""
    base_url = "http://127.0.0.1:5000"

    print("🚀 Testing Production Enhanced AI Agent API")
    print("=" * 60)

    # Test case with real OpenAI potential
    test_data = {
        "customer_id": "1001",
        "message": "Tôi muốn ăn món gì healthy và có protein cao?",
        "location": "10.762622,106.660172"
    }

    print(f"📋 Test Case: Production API Call")
    print(f"Customer: {test_data['customer_id']}")
    print(f"Message: {test_data['message']}")
    print(f"Location: {test_data['location']}")
    print("-" * 40)

    try:
        start_time = time.time()

        response = requests.post(
            f"{base_url}/api/enhanced-chat",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        end_time = time.time()
        response_time = end_time - start_time

        print(f"⏱️  Response time: {response_time:.2f}s")
        print(f"📊 Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"🤖 Agent Type: {data.get('agent_type', 'unknown')}")

            # Check if it's using real OpenAI or demo
            metrics = data.get('performance_metrics', {})
            data_sources = metrics.get('data_sources_used', '')

            if 'GPT' in data_sources and 'Demo' not in data_sources:
                print("🎯 REAL OPENAI API DETECTED!")
                print(f"🔥 Data Sources: {data_sources}")
            else:
                print("🔄 Using Demo/Fallback Mode")
                print(f"📊 Data Sources: {data_sources}")

            # Show response preview
            response_text = data.get('response', '')
            print(f"📝 Response Preview: {response_text[:100]}...")

            # Show processing steps
            steps = data.get('processing_steps', [])
            print("🔄 Processing Steps:")
            for step in steps:
                status_icon = "✅" if step['status'] == 'completed' else "🔄"
                print(f"   {status_icon} {step['title']}: {step['status']}")

            # Show performance metrics
            print("📊 Performance Metrics:")
            for key, value in metrics.items():
                print(f"   - {key}: {value}")

            print("\n🎯 Full Response Structure:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")

        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    test_production_api()
