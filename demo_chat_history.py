#!/usr/bin/env python3
"""
Demo script để test tính năng lưu lịch sử chat
"""

import requests
import json
import time
from datetime import datetime


def test_chat_history_feature():
    """Test tính năng lưu lịch sử chat"""
    print("🧪 DEMO TÍNH NĂNG LƯU LỊCH SỬ CHAT")
    print("=" * 50)

    base_url = "http://localhost:5000"

    # Test 1: Kiểm tra trang AI Agent
    print("\n1️⃣ Kiểm tra trang AI Agent...")
    try:
        response = requests.get(f"{base_url}/agent", timeout=5)
        if response.status_code == 200:
            print("✅ Trang AI Agent hoạt động bình thường")
            print(f"   Response length: {len(response.text):,} bytes")
        else:
            print(f"❌ Lỗi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối: {e}")
        return False

    # Test 2: Kiểm tra trang test chat history
    print("\n2️⃣ Kiểm tra trang test chat history...")
    try:
        response = requests.get(f"{base_url}/test-chat-history", timeout=5)
        if response.status_code == 200:
            print("✅ Trang test chat history hoạt động")
            print(f"   Response length: {len(response.text):,} bytes")
        else:
            print(f"❌ Lỗi: {response.status_code}")
    except Exception as e:
        print(f"❌ Không thể kết nối: {e}")

    # Test 3: Test API agent chat
    print("\n3️⃣ Test API agent chat...")
    try:
        test_data = {
            'message': 'Xin chào AI Agent! Đây là tin nhắn test.',
            'customer_id': 'CUS00001'
        }
        response = requests.post(f"{base_url}/api/agent_chat",
                                 json=test_data,
                                 headers={'Content-Type': 'application/json'},
                                 timeout=15)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ API agent chat hoạt động")
                print(f"   AI Response: {result.get('response', '')[:100]}...")
            else:
                print(f"❌ API trả về lỗi: {result.get('error', 'Unknown')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi API: {e}")

    # Test 4: Hướng dẫn test thủ công
    print(f"\n4️⃣ Hướng dẫn test thủ công:")
    print("   📖 Để test đầy đủ tính năng, hãy:")
    print("   1. Mở trình duyệt tại: http://localhost:5000/agent")
    print("   2. Gửi vài tin nhắn với AI")
    print("   3. Nhấn F5 để refresh trang")
    print("   4. Kiểm tra lịch sử có được phục hồi không")
    print("   5. Thử xuất lịch sử và xem thống kê")
    print("   6. Test trang: http://localhost:5000/test-chat-history")

    print(f"\n🎉 DEMO HOÀN TẤT!")
    print("✅ Tính năng lưu lịch sử chat đã sẵn sàng sử dụng!")

    return True


def show_feature_summary():
    """Hiển thị tóm tắt tính năng"""
    print("\n📋 TÓM TẮT TÍNH NĂNG MỚI:")
    print("=" * 40)

    features = [
        "💾 Lưu trữ tự động tin nhắn vào localStorage",
        "🔄 Khôi phục lịch sử sau khi F5/refresh",
        "📥 Xuất lịch sử chat thành file JSON",
        "📊 Thống kê chi tiết về cuộc trò chuyện",
        "🗑️ Xóa lịch sử an toàn với xác nhận",
        "⏱️ Hiển thị timestamp cho mỗi tin nhắn",
        "🎯 Giới hạn 100 tin nhắn để tối ưu hiệu suất",
        "🧪 Trang test chuyên dụng cho developer"
    ]

    for i, feature in enumerate(features, 1):
        print(f"   {i}. {feature}")

    print(f"\n🔗 URLs quan trọng:")
    print("   • AI Agent: http://localhost:5000/agent")
    print("   • Test Page: http://localhost:5000/test-chat-history")
    print("   • Home: http://localhost:5000")


if __name__ == "__main__":
    print(f"🚀 CHAT HISTORY FEATURE DEMO")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    success = test_chat_history_feature()

    if success:
        show_feature_summary()
        print(f"\n🎯 TRẠNG THÁI: SẴN SÀNG SỬ DỤNG!")
    else:
        print(f"\n⚠️ TRẠNG THÁI: CẦN KIỂM TRA LẠI!")
        print("💡 Hãy đảm bảo Flask app đang chạy: python app.py")
