"""
Test giao diện chi tiết AI Agent
"""

import requests
import json
import time


def test_detailed_interface():
    """Test giao diện chi tiết với real data"""
    base_url = "http://127.0.0.1:5000"

    print("🧠 Testing Detailed AI Agent Interface")
    print("=" * 60)

    # Test case thực tế để xem workflow chi tiết
    test_data = {
        "customer_id": "1001",
        "message": "Tôi muốn làm một món healthy cho gia đình, có protein cao và ít calories",
        "location": "10.762622,106.660172"
    }

    print(f"📋 Test Case: Detailed Analysis Request")
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

            # Show processing steps trong detail
            steps = data.get('processing_steps', [])
            print("\n🔄 Detailed Processing Steps:")
            for i, step in enumerate(steps, 1):
                print(f"   {i}. {step['title']}")
                print(f"      Status: {step['status']}")
                print(f"      Description: {step.get('description', 'N/A')}")
                print()

            # Show customer info
            customer_info = data.get('customer_info', {})
            print("👤 Customer Profile Analysis:")
            for key, value in customer_info.items():
                print(f"   - {key}: {value}")
            print()

            # Show performance metrics
            metrics = data.get('performance_metrics', {})
            print("📊 Performance Analysis:")
            for key, value in metrics.items():
                print(f"   - {key}: {value}")
            print()

            # Show context used
            context = data.get('context_used', '')
            print(f"🔍 Context Analysis: {context}")
            print()

            # Show response preview
            response_text = data.get('response', '')
            print(f"📝 AI Response Preview:")
            print(
                response_text[:200] + "..." if len(response_text) > 200 else response_text)
            print()

            print("🎯 How to Use Detailed Interface:")
            print("1. Truy cập: http://127.0.0.1:5000/agent-detailed")
            print("2. Chọn khách hàng từ dropdown")
            print("3. Nhập câu hỏi chi tiết")
            print("4. Click vào từng bước workflow để xem phân tích")
            print("5. Xem performance metrics real-time")
            print("6. Đọc JSON analysis trong từng step")

        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    test_detailed_interface()
