import openai
import json
import requests
from typing import Dict, List, Optional
import pandas as pd
from simple_food_db import SimpleFoodRecommendationDB
import os
from datetime import datetime

# Import cache manager
try:
    from cache_manager import cached, cache_manager
    CACHING_ENABLED = True
except ImportError:
    CACHING_ENABLED = False
    print("⚠️ Cache manager not available - running without caching")

    # Fallback decorator
    def cached(expire_hours: int = 24):
        def decorator(func):
            return func
        return decorator


class FoodAIAgent:
    def __init__(self, openai_api_key: str = None):
        """Initialize the Food AI Agent with OpenAI integration"""
        # Set OpenAI API key (you should set this as environment variable)
        if openai_api_key:
            openai.api_key = openai_api_key
        elif os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
        else:
            print("⚠️ Warning: OpenAI API key not provided. Some features may not work.")
          # Initialize simple database
        self.vector_db = SimpleFoodRecommendationDB()

        # Professional prompt for the AI agent
        self.system_prompt = """
        Bạn là một chuyên gia tư vấn ẩm thực và dinh dưỡng chuyên nghiệp, có nhiệm vụ đưa ra các gợi ý món ăn an toàn, hợp vệ sinh, phù hợp với từng nhóm người dùng. 

        MỤC TIÊU CHÍNH:
        - Giúp người tiêu dùng lựa chọn thực đơn vừa ngon miệng, vừa đảm bảo sức khỏe
        - Ưu tiên an toàn thực phẩm và vệ sinh dinh dưỡng
        - Tư vấn phù hợp với từng nhóm đối tượng (trẻ em, người già, người bệnh, v.v.)
        - Đưa ra giải pháp thực tế, sáng tạo và dễ thực hiện

        PHONG CÁCH TƯ VẤN:
        - Thân thiện, nhiệt tình và dễ hiểu
        - Dựa trên dữ liệu và nghiên cứu khoa học
        - Cung cấp thông tin chi tiết về dinh dưỡng
        - Đưa ra lựa chọn thay thế khi cần thiết

        LĨNH VỰC CHUYÊN MÔN:
        - Món ăn Việt Nam truyền thống và hiện đại
        - Dinh dưỡng cho các nhóm tuổi khác nhau
        - An toàn thực phẩm và vệ sinh
        - Chế độ ăn đặc biệt (giảm cân, tiểu đường, tim mạch, v.v.)        - Món ăn phù hợp với điều kiện địa phương

        Hãy luôn đưa ra lời khuyên có căn cứ và thực tế, ưu tiên sức khỏe của người dùng.
        """

    @cached(expire_hours=2)  # Cache for 2 hours
    def get_contextual_data(self, user_query: str, user_id: str = None) -> Dict:
        """Get relevant contextual data from vector database"""
        context_data = {
            "recipes": [],
            "customer_info": {},
            "recommendations": []
        }

        try:
            # Search for relevant recipes
            recipe_results = self.vector_db.search_recipes(
                user_query, n_results=8)
            if recipe_results and recipe_results['documents']:
                for i, (doc, meta) in enumerate(zip(recipe_results['documents'][0], recipe_results['metadatas'][0])):
                    context_data["recipes"].append({
                        "name": meta['recipe_name'],
                        "url": meta['recipe_url'],
                        "difficulty": meta['difficulty'],
                        "meal_time": meta['meal_time'],
                        "nutrition_category": meta['nutrition_category'],
                        "calories": meta['estimated_calories'],
                        "prep_time": meta['preparation_time_minutes'],
                        "ingredients": meta['ingredient_count'],
                        "price": meta['estimated_price_vnd'],
                        "rating": meta['avg_rating']
                    })

            # Get customer information if user_id provided
            if user_id:
                customer_results = self.vector_db.search_customers(
                    f"customer_id {user_id}", n_results=1)
                if customer_results and customer_results['metadatas']:
                    context_data["customer_info"] = customer_results['metadatas'][0][0]

        except Exception as e:
            print(f"Error getting contextual data: {str(e)}")

        return context_data

    def get_nearby_restaurants(self, location: str, food_type: str = "") -> List[Dict]:
        """Simulate getting nearby restaurants (Google Maps integration placeholder)"""
        # This is a placeholder for Google Maps API integration
        # In a real implementation, you would use Google Places API
        mock_restaurants = [
            {
                "name": "Quán Cơm Tấm Sài Gòn",
                "address": f"123 Đường ABC, {location}",
                "rating": 4.5,
                "price_range": "50,000 - 100,000 VND",
                "specialties": ["Cơm tấm", "Sườn nướng", "Chả trứng"],
                "distance": "0.5 km",
                "opening_hours": "7:00 - 22:00"
            },
            {
                "name": "Nhà Hàng Món Huế",
                "address": f"456 Đường XYZ, {location}",
                "rating": 4.3,
                "price_range": "80,000 - 150,000 VND",
                "specialties": ["Bún bò Huế", "Nem lụi", "Bánh khoái"],
                "distance": "0.8 km",
                "opening_hours": "8:00 - 21:30"
            },
            {
                "name": "Quán Phở Hà Nội",
                "address": f"789 Đường DEF, {location}",
                "rating": 4.7,
                "price_range": "40,000 - 80,000 VND",
                "specialties": ["Phở bò", "Phở gà", "Bún chả"],
                "distance": "1.2 km",
                "opening_hours": "6:00 - 23:00"
            }
        ]
        # Filter by food type if specified
        if food_type:
            filtered_restaurants = []
            for restaurant in mock_restaurants:
                if any(food_type.lower() in specialty.lower() for specialty in restaurant['specialties']):
                    filtered_restaurants.append(restaurant)
            return filtered_restaurants if filtered_restaurants else mock_restaurants

        return mock_restaurants

    def generate_ai_response(self, user_query: str, context_data: Dict, user_id: str = None) -> str:
        """Generate AI response using OpenAI API with contextual data"""
        try:
            # Prepare context information
            context_text = ""

            if context_data["recipes"]:
                context_text += "\n\nCÁC MÓN ĂN LIÊN QUAN:\n"
                for recipe in context_data["recipes"][:5]:  # Limit to top 5
                    context_text += f"- {recipe['name']}: {recipe['nutrition_category']}, {recipe['difficulty']}, {recipe['calories']} kcal, {recipe['prep_time']} phút\n"

            if context_data["customer_info"]:
                customer = context_data["customer_info"]
                context_text += f"\n\nTHÔNG TIN KHÁCH HÀNG:\n"
                context_text += f"- Tên: {customer.get('full_name', 'N/A')}\n"
                context_text += f"- Nhóm tuổi: {customer.get('age_group', 'N/A')}\n"
                context_text += f"- Khu vực: {customer.get('region', 'N/A')}\n"

            # Create the full prompt
            full_prompt = f"""
            {self.system_prompt}

            THÔNG TIN NGỮ CẢNH:
            {context_text}

            CÂU HỎI CỦA NGƯỜI DÙNG:
            {user_query}

            Hãy đưa ra lời tư vấn chi tiết, thực tế và hữu ích dựa trên thông tin ngữ cảnh trên.
            """

            # Call OpenAI API (if available) - Updated for OpenAI v1.0+
            if hasattr(openai, 'api_key') and openai.api_key:
                from openai import OpenAI
                client = OpenAI(api_key=openai.api_key)

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user",
                            "content": f"{context_text}\n\nCâu hỏi: {user_query}"}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            else:
                # Fallback response when OpenAI API is not available
                return self.generate_fallback_response(user_query, context_data)

        except Exception as e:
            print(f"Error generating AI response: {str(e)}")
            return self.generate_fallback_response(user_query, context_data)

    def generate_fallback_response(self, user_query: str, context_data: Dict) -> str:
        """Generate fallback response when OpenAI API is not available"""
        response = "🍽️ **Tư vấn món ăn từ chuyên gia dinh dưỡng**\n\n"

        # Analyze query for key topics
        query_lower = user_query.lower()

        if "sức khỏe" in query_lower or "dinh dưỡng" in query_lower:
            response += "**Về dinh dưỡng và sức khỏe:**\n"
            response += "- Ưu tiên các món giàu chất xơ, vitamin và khoáng chất\n"
            response += "- Hạn chế đồ chiên rán, nhiều dầu mỡ\n"
            response += "- Cân bằng protein, carb và chất béo tốt\n\n"

        if "tiểu đường" in query_lower or "đường huyết" in query_lower:
            response += "**Dành cho người tiểu đường:**\n"
            response += "- Chọn món ít đường, ít tinh bột\n"
            response += "- Tăng cường rau xanh, protein nạc\n"
            response += "- Chia nhỏ bữa ăn trong ngày\n\n"

        if "dễ làm" in query_lower or "dễ chế biến" in query_lower:
            response += "**Món ăn dễ chế biến:**\n"
            response += "- Các món luộc, hấp đơn giản\n"
            response += "- Salad, gỏi tươi mát\n"
            response += "- Canh chua, soup dinh dưỡng\n\n"

        # Add relevant recipes from context
        if context_data["recipes"]:
            response += "**Gợi ý món ăn phù hợp:**\n"
            for i, recipe in enumerate(context_data["recipes"][:3], 1):
                response += f"{i}. **{recipe['name']}**\n"
                response += f"   - Độ khó: {recipe['difficulty']}\n"
                response += f"   - Thời gian: {recipe['prep_time']} phút\n"
                response += f"   - Calories: {recipe['calories']} kcal\n"
                response += f"   - Phù hợp: {recipe['nutrition_category']}\n\n"

        # Add customer-specific advice
        if context_data["customer_info"]:
            customer = context_data["customer_info"]
            age_group = customer.get('age_group', '')
            region = customer.get('region', '')

            response += f"**Lời khuyên cá nhân hóa:**\n"
            if age_group:
                if "18-24" in age_group:
                    response += "- Phù hợp với lứa tuổi trẻ: cần nhiều năng lượng, đa dạng món ăn\n"
                elif "65+" in age_group:
                    response += "- Phù hợp cho người cao tuổi: dễ tiêu hóa, mềm, bổ dưỡng\n"
                else:
                    response += "- Cân bằng dinh dưỡng theo độ tuổi, chú ý sức khỏe tim mạch\n"

            if region:
                response += f"- Món ăn địa phương {region}: tận dụng nguyên liệu tươi sẵn có\n"

        response += "\n💡 **Lời khuyên chung:**\n"
        response += "- Luôn chọn nguyên liệu tươi, sạch\n"
        response += "- Đảm bảo vệ sinh an toàn thực phẩm\n"
        response += "- Cân bằng các nhóm chất dinh dưỡng\n"
        response += "- Uống đủ nước, ăn đúng giờ\n"

        return response

    @cached(expire_hours=1)
    def process_user_request(self, user_query: str, user_id: str = None, location: str = None) -> Dict:
        """Main method to process user request and return comprehensive response"""
        try:
            # Get contextual data from vector database
            context_data = self.get_contextual_data(user_query, user_id)

            # Generate AI response
            ai_response = self.generate_ai_response(
                user_query, context_data, user_id)

            # Get nearby restaurants if location provided
            nearby_restaurants = []
            if location:
                # Extract food type from query for restaurant filtering
                food_keywords = ["phở", "cơm", "bún",
                                 "bánh", "chả", "gỏi", "salad"]
                food_type = ""
                for keyword in food_keywords:
                    if keyword in user_query.lower():
                        food_type = keyword
                        break

                nearby_restaurants = self.get_nearby_restaurants(
                    location, food_type)

            return {
                "ai_response": ai_response,
                "recommended_recipes": context_data["recipes"][:5],
                "customer_info": context_data["customer_info"],
                "nearby_restaurants": nearby_restaurants,
                "timestamp": datetime.now().isoformat(),
                "query": user_query
            }

        except Exception as e:
            return {
                "ai_response": f"Xin lỗi, đã có lỗi xảy ra: {str(e)}. Vui lòng thử lại sau.",
                "recommended_recipes": [],
                "customer_info": {},
                "nearby_restaurants": [],
                "timestamp": datetime.now().isoformat(),
                "query": user_query,
                "error": str(e)
            }

# Utility functions for the Flask app


def get_agent_instance():
    """Get singleton instance of the AI agent"""
    if not hasattr(get_agent_instance, '_instance'):
        get_agent_instance._instance = FoodAIAgent()
    return get_agent_instance._instance
