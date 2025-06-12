#!/usr/bin/env python3
"""
Kiểm tra đầy đủ xem hệ thống đã load 14,953 interactions chưa
"""

import sqlite3
import os
import requests
import json
from datetime import datetime


def kiem_tra_database():
    """Kiểm tra database SQLite"""
    print("🔍 KIỂM TRA DATABASE SQLite")
    print("=" * 40)

    db_path = './simple_food_db.sqlite'
    if not os.path.exists(db_path):
        print("❌ Không tìm thấy file database!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Đếm số lượng records
    cursor.execute('SELECT COUNT(*) FROM recipes')
    recipes_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM customers')
    customers_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM interactions')
    interactions_count = cursor.fetchone()[0]

    print(f"📊 SỐ LIỆU HIỆN TẠI:")
    print(f"   🍽️  Recipes (công thức): {recipes_count:,}")
    print(f"   👥 Customers (khách hàng): {customers_count:,}")
    print(f"   💬 Interactions (tương tác): {interactions_count:,}")

    # Kiểm tra mục tiêu 14,953
    target = 14953
    if interactions_count == target:
        print(
            f"\n🎉 THÀNH CÔNG! Đã load đủ {interactions_count:,} interactions!")
        status = "✅ HOÀN THÀNH"
    elif interactions_count > 0:
        missing = target - interactions_count
        print(f"\n⚠️  THIẾU: {missing:,} interactions")
        print(f"   Hiện có: {interactions_count:,}/{target:,}")
        status = "🔄 CHƯA ĐỦ"
    else:
        print(f"\n❌ CHƯA LOAD: Không có interactions nào!")
        status = "❌ CHƯA LOAD"

    # Kiểm tra chất lượng dữ liệu
    if interactions_count > 0:
        print(f"\n📈 CHẤT LƯỢNG DỮ LIỆU:")

        # Unique customers và recipes
        cursor.execute('SELECT COUNT(DISTINCT customer_id) FROM interactions')
        unique_customers = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(DISTINCT recipe_name) FROM interactions')
        unique_recipes = cursor.fetchone()[0]

        print(f"   - Khách hàng unique: {unique_customers:,}")
        print(f"   - Công thức unique: {unique_recipes:,}")

        # Rating distribution
        cursor.execute(
            'SELECT AVG(rating), MIN(rating), MAX(rating) FROM interactions WHERE rating > 0')
        avg_rating, min_rating, max_rating = cursor.fetchone()
        if avg_rating:
            print(
                f"   - Đánh giá TB: {avg_rating:.2f} (từ {min_rating} đến {max_rating})")

        # Mẫu dữ liệu gần đây
        print(f"\n📋 MẪU DỮ LIỆU GẦN ĐÂY:")
        cursor.execute('''
            SELECT customer_id, recipe_name, rating, interaction_date 
            FROM interactions 
            ORDER BY interaction_date DESC 
            LIMIT 3
        ''')
        samples = cursor.fetchall()
        for i, (customer_id, recipe_name, rating, date) in enumerate(samples, 1):
            print(f"   {i}. {customer_id}: {recipe_name} (⭐{rating}, {date})")

    conn.close()
    return interactions_count == target, status


def kiem_tra_flask_app():
    """Kiểm tra Flask application"""
    print(f"\n🌐 KIỂM TRA FLASK APPLICATION")
    print("=" * 40)

    try:
        # Test API stats
        response = requests.get(
            'http://localhost:5000/api/agent_stats', timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Flask App đang chạy!")
            print("📊 API Stats:")
            print(f"   - Recipes: {stats.get('recipes_count', 'N/A')}")
            print(f"   - Customers: {stats.get('customers_count', 'N/A')}")
            if 'dataset_info' in stats:
                print(f"   - Dataset: {stats['dataset_info']}")

            # Test AI Agent
            print(f"\n🤖 TEST AI AGENT:")
            test_data = {
                'message': 'Hệ thống có bao nhiêu dữ liệu tương tác khách hàng?',
                'customer_id': 'CUS00001'
            }
            chat_response = requests.post('http://localhost:5000/api/agent_chat',
                                          json=test_data,
                                          headers={
                                              'Content-Type': 'application/json'},
                                          timeout=15)
            if chat_response.status_code == 200:
                result = chat_response.json()
                agent_response = result.get('response', '')
                print(f"✅ AI Agent phản hồi ({len(agent_response)} ký tự):")
                print(f"   {agent_response[:150]}...")
                return True, "✅ HOẠT ĐỘNG"
            else:
                print(f"❌ AI Agent lỗi: {chat_response.status_code}")
                return False, "❌ LỖI API"
        else:
            print(f"❌ Flask App không phản hồi: {response.status_code}")
            return False, "❌ KHÔNG PHẢN HỒI"
    except Exception as e:
        print(f"⚠️  Flask App không chạy: {e}")
        print("💡 Để khởi động: python app.py")
        return False, "⚠️ KHÔNG CHẠY"


def main():
    print("🚀 KIỂM TRA HỆ THỐNG AI FOOD RECOMMENDATION")
    print("=" * 60)
    print(f"📅 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Kiểm tra database
    db_success, db_status = kiem_tra_database()

    # Kiểm tra Flask app
    app_success, app_status = kiem_tra_flask_app()

    # Tổng kết
    print(f"\n📋 TỔNG KẾT KIỂM TRA")
    print("=" * 30)
    print(f"💾 Database: {db_status}")
    print(f"🌐 Flask App: {app_status}")

    if db_success and app_success:
        print(f"\n🎉 KẾT LUẬN: HỆ THỐNG HOÀN CHỈNH!")
        print("✅ Đã load đủ 14,953 interactions")
        print("✅ Flask app hoạt động bình thường")
        print("✅ AI Agent sẵn sàng phục vụ")
        print("🚀 READY FOR PRODUCTION!")
    elif db_success:
        print(f"\n🔄 KẾT LUẬN: DATABASE OK, CẦN KHỞI ĐỘNG APP")
        print("✅ Dữ liệu đã load đầy đủ")
        print("⚠️  Cần chạy Flask app: python app.py")
    else:
        print(f"\n⚠️  KẾT LUẬN: CẦN HOÀN THIỆN LOAD DỮ LIỆU")
        print("🔄 Chạy script load dữ liệu: python load_all_interactions.py")


if __name__ == "__main__":
    main()
