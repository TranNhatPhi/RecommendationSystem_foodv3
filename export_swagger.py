#!/usr/bin/env python3
"""
Export Swagger/OpenAPI specification to JSON file
"""

import json
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import app, api

    def export_swagger_json():
        """Export the Swagger specification to a JSON file"""
        with app.app_context():
            # Get the Swagger JSON
            swagger_json = api.__schema__

            # Write to file
            with open('swagger_spec.json', 'w', encoding='utf-8') as f:
                json.dump(swagger_json, f, indent=2, ensure_ascii=False)

            print("✅ Swagger specification exported to swagger_spec.json")
            return swagger_json

    def print_api_summary():
        """Print a summary of all available endpoints"""
        print("\n" + "="*60)
        print("🍽️  VIETNAMESE FOOD RECOMMENDATION SYSTEM API")
        print("="*60)
        print("📚 Swagger UI: http://localhost:5000/swagger/")
        print("📄 API Docs: http://localhost:5000/api-docs")
        print("🧪 Test Page: file:///d:/savecode/RecommendationSystemv5/test_swagger_endpoints.html")
        print("\n📋 AVAILABLE ENDPOINTS:")
        print("-"*60)

        endpoints = [
            ("GET", "/api/upsell_combos", "Gợi ý combo món ăn"),
            ("GET", "/api/upsell_sides", "Gợi ý món phụ"),
            ("GET", "/api/family_combos", "Combo gia đình"),
            ("GET", "/api/age_based_recommendations", "Gợi ý theo độ tuổi"),
            ("GET", "/api/meal_recommendations", "Gợi ý theo bữa ăn"),
            ("GET", "/api/meal_plans", "Thực đơn hoàn chỉnh"),
            ("GET", "/api/nutrition_recommendations", "Gợi ý dinh dưỡng"),
        ]

        for method, endpoint, description in endpoints:
            print(f"{method:4} {endpoint:35} - {description}")

        print("\n🔧 EXAMPLE REQUESTS:")
        print("-"*60)
        print(
            "curl -X GET 'http://localhost:5000/api/upsell_combos?user_id=12345&item_id=54'")
        print("curl -X GET 'http://localhost:5000/api/family_combos?user_id=12345&family_size=4'")
        print("curl -X GET 'http://localhost:5000/api/nutrition_recommendations?user_id=12345&nutrition_type=weight-loss'")

        print("\n🧪 TESTING:")
        print("-"*60)
        print("1. Mở Swagger UI: http://localhost:5000/swagger/")
        print("2. Mở Test Page: test_swagger_endpoints.html")
        print("3. Hoặc sử dụng curl/Postman với các endpoint trên")

        print("\n" + "="*60)

    if __name__ == '__main__':
        export_swagger_json()
        print_api_summary()

except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Make sure the server is not running and try again")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
