"""
Test Enhanced AI Agent API
Kiểm tra tính năng Enhanced Chat API với demo agent
"""

import requests
import json
import time


def test_enhanced_chat_api():
    """Test Enhanced Chat API"""
    print("🚀 Testing Enhanced AI Agent API")
    print("=" * 50)

    # Test cases
    test_cases = [
        {
            "name": "Healthy Food Recommendation",
            "customer_id": "1001",
            "message": "Tôi muốn ăn món gì healthy và ngon?",
            "location": "10.762622,106.660172"  # Ho Chi Minh City
        },
        {
            "name": "Vietnamese Food Recommendation",
            "customer_id": "1002",
            "message": "Gợi ý cho tôi món Việt Nam truyền thống",
            "location": "21.028511,105.804817"  # Hanoi
        },
        {
            "name": "General Food Recommendation",
            "customer_id": "1003",
            "message": "Hôm nay tôi nên ăn gì?",
            "location": None
        }
    ]

    base_url = "http://127.0.0.1:5000"

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 40)

        # Prepare request data
        data = {
            "message": test_case["message"],
            "customer_id": test_case["customer_id"],
            "location": test_case["location"]
        }

        try:
            print(f"🔄 Sending request...")
            print(f"   Customer: {data['customer_id']}")
            print(f"   Message: {data['message']}")
            print(f"   Location: {data['location']}")

            start_time = time.time()

            # Send POST request
            response = requests.post(
                f"{base_url}/api/enhanced-chat",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            end_time = time.time()
            response_time = round(end_time - start_time, 2)

            print(f"⏱️  Response time: {response_time}s")
            print(f"📊 Status code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                print("✅ SUCCESS!")
                print(f"🤖 Agent Type: {result.get('agent_type', 'unknown')}")
                print(
                    f"📝 Response Preview: {result.get('response', '')[:100]}...")

                # Show processing steps
                if result.get('processing_steps'):
                    print("🔄 Processing Steps:")
                    for step in result['processing_steps']:
                        print(
                            f"   - {step.get('title', 'Unknown')}: {step.get('status', 'unknown')}")

                # Show performance metrics
                if result.get('performance_metrics'):
                    metrics = result['performance_metrics']
                    print("📊 Performance Metrics:")
                    for key, value in metrics.items():
                        print(f"   - {key}: {value}")

                # Show customer info
                if result.get('customer_info'):
                    customer = result['customer_info']
                    print(f"👤 Customer: {customer.get('name', 'Unknown')}")

                print("🎯 Full Response:")
                print(json.dumps(result, ensure_ascii=False, indent=2))

            else:
                print(f"❌ FAILED with status {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

        print("\n" + "="*50)


def test_basic_routes():
    """Test basic routes"""
    print("\n🔍 Testing Basic Routes")
    print("=" * 30)

    routes = [
        "/",
        "/ai-agent",
        "/agent"
    ]

    base_url = "http://127.0.0.1:5000"

    for route in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {route}: OK ({len(response.content)} bytes)")
            else:
                print(f"❌ {route}: {response.status_code}")
        except Exception as e:
            print(f"❌ {route}: {e}")


def main():
    print("🎯 Enhanced AI Agent API Testing Suite")
    print("=" * 60)

    # Test basic routes first
    test_basic_routes()

    # Test enhanced chat API
    test_enhanced_chat_api()

    print("\n🎉 Testing Complete!")
    print("=" * 60)

    print("\n📋 Summary:")
    print("- Enhanced AI Agent API với demo mode")
    print("- Tích hợp workflow visualization")
    print("- Support cho location-based recommendations")
    print("- Performance metrics tracking")
    print("- Customer profile integration")

    print("\n🔧 Next Steps:")
    print("1. Cập nhật API keys trong .env để sử dụng GPT-4")
    print("2. Test trên production với real LLM")
    print("3. Tích hợp Google Maps API")
    print("4. Setup ChromaDB với production data")


if __name__ == "__main__":
    main()
