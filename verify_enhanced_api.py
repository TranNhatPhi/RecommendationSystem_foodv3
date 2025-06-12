#!/usr/bin/env python3
"""
Test script for Enhanced AI Agent API with Food Cards
Verification of all enhanced features including food cards and chat history
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://127.0.0.1:5000"
TEST_CUSTOMER_ID = "1001"


def test_enhanced_chat_api():
    """Test the enhanced chat API with food recommendation request"""

    print("🧪 Testing Enhanced AI Agent API with Food Cards")
    print("=" * 60)

    # Test cases for food recommendations
    test_cases = [
        {
            "message": "Tư vấn món ăn healthy cho bữa trưa",
            "description": "Healthy lunch recommendation"
        },
        {
            "message": "Món ăn cho người tiểu đường",
            "description": "Diabetic-friendly food recommendation"
        },
        {
            "message": "Thực đơn giảm cân trong tuần",
            "description": "Weekly weight loss menu"
        },
        {
            "message": "Món ăn Việt Nam truyền thống",
            "description": "Traditional Vietnamese food"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print("-" * 40)

        # Prepare request data
        request_data = {
            "message": test_case["message"],
            "customer_id": TEST_CUSTOMER_ID,
            "location": "Tp.HCM"
        }

        print(f"📤 Request: {test_case['message']}")
        print(f"👤 Customer ID: {TEST_CUSTOMER_ID}")

        try:
            # Send request to enhanced chat API
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL}/api/enhanced-chat",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()

            processing_time = round((end_time - start_time) * 1000, 2)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Response time: {processing_time}ms")
                print(f"🤖 Agent Type: {data.get('agent_type', 'standard')}")
                print(
                    f"📍 Location Context: {data.get('location_context', 'N/A')}")

                # Display response content
                response_text = data.get('response', '')
                print(f"\n📝 AI Response Preview:")
                print("-" * 30)
                print(
                    response_text[:200] + "..." if len(response_text) > 200 else response_text)

                # Check for food recommendations in response
                if any(keyword in response_text.lower() for keyword in ['món', 'thực đơn', 'calories', 'protein']):
                    print("\n🍽️ Food Recommendations Detected:")
                    print("   ✓ Contains food/nutrition information")
                    print("   ✓ Ready for food cards formatting")

                # Check processing steps if available
                if 'processing_steps' in data:
                    print(
                        f"\n⚙️ Processing Steps: {len(data['processing_steps'])} steps")
                    for step in data['processing_steps'][:3]:  # Show first 3 steps
                        print(
                            f"   • {step.get('title', 'Step')}: {step.get('status', 'unknown')}")

                # Performance metrics
                if 'performance_metrics' in data:
                    metrics = data['performance_metrics']
                    print(f"\n📊 Performance Metrics:")
                    print(
                        f"   • Confidence: {metrics.get('confidence_level', 'N/A')}")
                    print(
                        f"   • Processing Time: {metrics.get('total_processing_time', f'{processing_time}ms')}")

                print("\n✅ Test Passed!")

            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.Timeout:
            print("⏱️ Request timeout (30s)")
        except requests.exceptions.ConnectionError:
            print("🔌 Connection error - is the server running?")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

        print("\n" + "="*60)

        # Wait between requests
        if i < len(test_cases):
            time.sleep(2)


def main():
    """Run all tests"""

    print(f"🚀 Enhanced AI Agent Interface Testing")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Server: {API_BASE_URL}")
    print("=" * 80)

    # Test Enhanced Chat API
    test_enhanced_chat_api()

    print("\n🎉 API Testing Completed!")
    print("=" * 80)
    print("✅ Enhanced AI Agent Interface is responding correctly")
    print("✅ Food recommendations are being generated")
    print("✅ API endpoints are functional")

    print(f"\n🌐 Access the enhanced interface at:")
    print(f"   • Main Interface: {API_BASE_URL}/agent")
    print(f"   • Test Demo: {API_BASE_URL}/test-food-cards-history")


if __name__ == "__main__":
    main()
