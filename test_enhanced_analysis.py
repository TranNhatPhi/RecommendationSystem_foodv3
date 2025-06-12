"""
Test Enhanced Analysis Interface - Chi tiết phân tích quy trình AI
"""

import requests
import json
import time


def test_enhanced_analysis():
    """Test giao diện phân tích chi tiết mới"""
    base_url = "http://127.0.0.1:5000"

    print("🧠 Testing Enhanced Analysis Interface")
    print("=" * 60)

    # Test cases với các loại câu hỏi khác nhau để xem phân tích
    test_cases = [
        {
            "customer_id": "1001",
            "message": "Phân tích món healthy có protein cao cho gia đình 4 người",
            "location": "10.762622,106.660172",
            "name": "Healthy Family Analysis"
        },
        {
            "customer_id": "1002",
            "message": "Gợi ý món Việt truyền thống với ngân sách dưới 200k",
            "location": "21.028511,105.804817",
            "name": "Vietnamese Traditional Analysis"
        },
        {
            "customer_id": "1003",
            "message": "Thực đơn giảm cân cho người tiểu đường trong 1 tuần",
            "location": None,
            "name": "Diet Plan Analysis"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print(f"Customer: {test_case['customer_id']}")
        print(f"Message: {test_case['message']}")
        print(f"Location: {test_case['location'] or 'None'}")
        print("-" * 50)

        try:
            start_time = time.time()

            response = requests.post(
                f"{base_url}/api/enhanced-chat",
                json={
                    "customer_id": test_case["customer_id"],
                    "message": test_case["message"],
                    "location": test_case["location"]
                },
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

                # Show processing steps analysis
                steps = data.get('processing_steps', [])
                print(f"\n🔄 Workflow Analysis ({len(steps)} steps):")
                for j, step in enumerate(steps, 1):
                    print(f"   {j}. {step['title']}")
                    print(f"      ├─ Status: {step['status']}")
                    print(
                        f"      ├─ Description: {step.get('description', 'N/A')}")
                    if 'id' in step:
                        print(f"      └─ ID: {step['id']}")
                    print()

                # Show detailed customer analysis
                customer_info = data.get('customer_info', {})
                if customer_info:
                    print("👤 Customer Analysis:")
                    print(f"   ├─ Name: {customer_info.get('name', 'N/A')}")
                    print(f"   ├─ Age: {customer_info.get('age', 'N/A')}")
                    print(
                        f"   ├─ Location: {customer_info.get('location', 'N/A')}")
                    print(
                        f"   ├─ Preferences: {customer_info.get('preferences', [])}")
                    print(
                        f"   └─ Restrictions: {customer_info.get('restrictions', [])}")
                    print()

                # Show context analysis
                context = data.get('context_used', '')
                if context:
                    print(f"🔍 Context Analysis:")
                    print(f"   └─ {context}")
                    print()

                # Show performance metrics
                metrics = data.get('performance_metrics', {})
                if metrics:
                    print("📊 Performance Metrics:")
                    for key, value in metrics.items():
                        print(f"   ├─ {key}: {value}")
                    print()

                # Show response summary
                response_text = data.get('response', '')
                print(f"📝 AI Response Summary:")
                summary = response_text[:150] + \
                    "..." if len(response_text) > 150 else response_text
                print(f"   └─ {summary}")
                print()

            else:
                print(f"❌ FAILED! Status: {response.status_code}")
                print(f"Error: {response.text}")

        except Exception as e:
            print(f"❌ ERROR: {e}")

        if i < len(test_cases):
            print("\n" + "="*60)

    # Summary và hướng dẫn sử dụng
    print("\n🎯 Enhanced Analysis Interface Guide:")
    print("=" * 60)
    print("1. Truy cập: http://127.0.0.1:5000/agent-analysis")
    print("2. Chọn khách hàng từ dropdown")
    print("3. Nhập câu hỏi chi tiết để phân tích")
    print("4. Xem workflow steps real-time")
    print("5. Click vào từng step để xem:")
    print("   ├─ Mô tả chi tiết")
    print("   ├─ Kỹ thuật sử dụng")
    print("   ├─ Dữ liệu real-time")
    print("   └─ JSON analysis data")
    print("6. Theo dõi performance metrics")
    print("7. Xem customer profile analysis")
    print()
    print("🔥 Key Features:")
    print("├─ Real-time workflow visualization")
    print("├─ Expandable step-by-step analysis")
    print("├─ JSON data viewer cho từng step")
    print("├─ Performance metrics dashboard")
    print("├─ Customer profile integration")
    print("├─ Context analysis display")
    print("└─ Enhanced UI với animations")
    print()
    print("💡 Tips:")
    print("├─ Sử dụng câu hỏi cụ thể để xem phân tích chi tiết")
    print("├─ Click chevron icon để mở rộng từng step")
    print("├─ Xem JSON viewer để hiểu dữ liệu raw")
    print("└─ Theo dõi processing time cho từng step")


if __name__ == "__main__":
    test_enhanced_analysis()
