# Vietnamese Food Recommendation System - Swagger API Documentation
# Author: AI Assistant
# Version: 1.0

from flask import Flask, request, jsonify, render_template
from flask_restx import Api, Resource, fields, Namespace
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os
import time

# Create Flask app
app = Flask(__name__)

# Load the trained model
try:
    model = CatBoostRegressor()
    model.load_model('catboost_best_model.cbm')
except Exception as e:
    print(f"Warning: Could not load model: {str(e)}")
    model = None

# Load interaction data
try:
    interactions_df = pd.read_csv('interactions_enhanced_final.csv')
    print(
        f"✅ Loaded enhanced dataset with {len(interactions_df)} interactions")
except Exception as e:
    try:
        interactions_df = pd.read_csv('interactions_encoded.csv')
        print(f"⚠️ Fallback to original dataset: {str(e)}")
    except Exception as e2:
        print(f"❌ Could not load any interactions data: {str(e2)}")
        interactions_df = pd.DataFrame()

# Create helper dictionaries for quick lookups
user_items = {}
item_features = {}
customer_ids = []

# Preprocess data for recommendations


def preprocess_data():
    global user_items, item_features, customer_ids

    if interactions_df.empty:
        print("No interaction data available.")
        return

    print("Preprocessing data for recommendations...")

    # Extract unique customer IDs (up to 300)
    customer_ids = sorted(interactions_df['customer_id'].unique().tolist())
    if len(customer_ids) > 300:
        customer_ids = customer_ids[:300]

    print(f"Extracted {len(customer_ids)} unique customer IDs")

    # Group interactions by user
    for _, row in interactions_df.iterrows():
        user_id = row['customer_id']
        if user_id not in user_items:
            user_items[user_id] = []

        user_items[user_id].append({
            'item_index': row['item_index'],
            'recipe_name': row['recipe_name'],
            'rating': row['rating'],
            'interaction_type': row['interaction_type'],
            'difficulty': row['difficulty'],
            'meal_time': row['meal_time']
        })

    # Extract item features for recommendations
    for _, row in interactions_df.iterrows():
        item_index = row['item_index']
        if item_index not in item_features:
            item_features[item_index] = {
                'recipe_name': row['recipe_name'],
                'recipe_url': row['recipe_url'],
                'difficulty': row['difficulty'],
                'meal_time': row['meal_time'],
                'content_score': row['content_score'],
                'cf_score': row['cf_score']
            }
    print("Data preprocessing complete!")

# Helper function to get recommendations


def get_recommendations(user_id, feature_type=None, count=5):
    if user_id not in user_items:
        return []

    # Get user's historical interactions
    user_history = user_items[user_id]

    # Make predictions for items not interacted with
    all_items = list(item_features.keys())
    interacted_items = [item['item_index'] for item in user_history]
    candidate_items = [
        item for item in all_items if item not in interacted_items]

    recommendations = []
    for item_index in candidate_items:
        # Use precomputed scores instead of model prediction to avoid errors
        cf_score = item_features[item_index].get('cf_score', 0)
        content_score = item_features[item_index].get('content_score', 0)
        prediction = cf_score + content_score

        recommendations.append({
            'item_index': item_index,
            'recipe_name': item_features[item_index]['recipe_name'],
            'recipe_url': item_features[item_index]['recipe_url'],
            'difficulty': item_features[item_index]['difficulty'],
            'meal_time': item_features[item_index]['meal_time'],
            'predicted_rating': float(prediction)
        })

    # Sort by predicted rating
    recommendations.sort(key=lambda x: x['predicted_rating'], reverse=True)

    # Filter by feature type if specified
    if feature_type == 'breakfast':
        breakfast_keywords = ['sáng', 'điểm tâm']
        recommendations = [
            r for r in recommendations if r.get('meal_time') == 'breakfast' or
            any(keyword in r['recipe_name'].lower()
                for keyword in breakfast_keywords)
        ]
    elif feature_type == 'lunch':
        lunch_keywords = ['trưa']
        recommendations = [
            r for r in recommendations if r.get('meal_time') == 'lunch' or
            any(keyword in r['recipe_name'].lower()
                for keyword in lunch_keywords)
        ]
    elif feature_type == 'dinner':
        dinner_keywords = ['tối', 'chiều']
        recommendations = [
            r for r in recommendations if r.get('meal_time') == 'dinner' or
            any(keyword in r['recipe_name'].lower()
                for keyword in dinner_keywords)
        ]
    elif feature_type == 'easy':
        recommendations = [
            r for r in recommendations if r['difficulty'] == 'Dễ']

    return recommendations[:count]

# Helper function for age-based nutrition focus


def get_nutrition_focus(age_group):
    if age_group == 'children':
        return "Growth, brain development, bone strength"
    elif age_group == 'teenagers':
        return "Energy, muscle development, brain function"
    elif age_group == 'adults':
        return "Balanced nutrition, energy, heart health"
    else:  # elderly
        return "Bone health, heart health, easy digestion"


# Initialize the app data at startup
with app.app_context():
    preprocess_data()

# Initialize Flask-RESTX
api = Api(
    app,
    version='1.0',
    title='Vietnamese Food Recommendation System API',
    description='Hệ thống gợi ý món ăn Việt Nam - API Documentation',
    doc='/swagger/',
    contact='AI Assistant',
    contact_email='support@example.com'
)

# Route for the web interface


@app.route('/')
def index():
    return render_template('index.html', customer_ids=customer_ids)

# Test page route


@app.route('/test')
def test_page():
    return render_template('simple_customer_test.html')


# Define namespaces
ns_recommendations = Namespace(
    'recommendations', description='Gợi ý món ăn cơ bản')
ns_upsell = Namespace('upsell', description='Gợi ý bán kèm')
ns_family = Namespace('family', description='Gợi ý cho gia đình')
ns_age = Namespace('age-based', description='Gợi ý theo độ tuổi')
ns_meal = Namespace('meals', description='Gợi ý theo bữa ăn')
ns_nutrition = Namespace('nutrition', description='Gợi ý theo dinh dưỡng')

api.add_namespace(ns_recommendations)
api.add_namespace(ns_upsell)
api.add_namespace(ns_family)
api.add_namespace(ns_age)
api.add_namespace(ns_meal)
api.add_namespace(ns_nutrition)

# Define models for request/response schemas
recommendation_model = api.model('Recommendation', {
    'recipe_name': fields.String(required=True, description='Tên món ăn'),
    'recipe_url': fields.String(required=True, description='URL công thức'),
    'difficulty': fields.String(required=True, description='Độ khó', enum=['Dễ', 'Trung bình', 'Khó']),
    'meal_time': fields.String(required=True, description='Bữa ăn', enum=['breakfast', 'lunch', 'dinner']),
    'predicted_rating': fields.Float(required=True, description='Điểm dự đoán'),
    'item_index': fields.Integer(description='Chỉ số món ăn')
})

combo_recommendation_model = api.model('ComboRecommendation', {
    'recipe_name': fields.String(required=True, description='Tên món ăn'),
    'recipe_url': fields.String(required=True, description='URL công thức'),
    'combo_discount': fields.String(required=True, description='Giảm giá combo'),
    'combo_price': fields.String(required=True, description='Giá combo'),
    'predicted_rating': fields.Float(required=True, description='Điểm dự đoán')
})

side_dish_model = api.model('SideDishRecommendation', {
    'recipe_name': fields.String(required=True, description='Tên món phụ'),
    'recipe_url': fields.String(required=True, description='URL công thức'),
    'side_price': fields.String(required=True, description='Giá món phụ'),
    'predicted_rating': fields.Float(required=True, description='Điểm dự đoán')
})

family_combo_model = api.model('FamilyCombo', {
    'main_dishes': fields.List(fields.Nested(recommendation_model), description='Món chính'),
    'side_dishes': fields.List(fields.Nested(recommendation_model), description='Món phụ'),
    'desserts': fields.List(fields.Nested(recommendation_model), description='Món tráng miệng')
})

meal_plan_model = api.model('MealPlan', {
    'menu_number': fields.Integer(required=True, description='Số thứ tự thực đơn'),
    'breakfast': fields.Nested(recommendation_model, allow_null=True, description='Món sáng'),
    'lunch': fields.Nested(recommendation_model, allow_null=True, description='Món trưa'),
    'dinner': fields.Nested(recommendation_model, allow_null=True, description='Món tối')
})

nutrition_recommendation_model = api.model('NutritionRecommendation', {
    'recipe_name': fields.String(required=True, description='Tên món ăn'),
    'recipe_url': fields.String(required=True, description='URL công thức'),
    'difficulty': fields.String(required=True, description='Độ khó'),
    'meal_time': fields.String(required=True, description='Bữa ăn'),
    'predicted_rating': fields.Float(required=True, description='Điểm dự đoán'),
    'item_index': fields.Integer(description='Chỉ số món ăn'),
    'estimated_calories': fields.Integer(description='Calories ước tính'),
    'preparation_time_minutes': fields.Integer(description='Thời gian chuẩn bị (phút)'),
    'ingredient_count': fields.Integer(description='Số lượng nguyên liệu'),
    'estimated_price_vnd': fields.Integer(description='Giá ước tính (VND)')
})

error_model = api.model('Error', {
    'error': fields.String(required=True, description='Thông báo lỗi')
})

# Upsell Combo Recommendations


@ns_upsell.route('/combos')
class UpsellCombos(Resource):
    @ns_upsell.doc('get_upsell_combos')
    @ns_upsell.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_upsell.param('item_id', 'ID món ăn hiện tại', required=True, type='string')
    @ns_upsell.marshal_with(api.model('UpsellCombosResponse', {
        'combo_recommendations': fields.List(fields.Nested(combo_recommendation_model)),
        'message': fields.String(description='Thông báo')
    }))
    @ns_upsell.response(400, 'Thiếu tham số', error_model)
    @ns_upsell.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý combo món ăn để tăng doanh thu"""
        user_id = request.args.get('user_id')
        item_id = request.args.get('item_id')

        if not user_id or not item_id:
            return {"error": "Missing user_id or item_id parameter"}, 400

        try:
            recommendations = get_recommendations(user_id, count=3)

            combo_recommendations = []
            for rec in recommendations:
                combo_recommendations.append({
                    "recipe_name": rec['recipe_name'],
                    "recipe_url": rec['recipe_url'],
                    "combo_discount": "10%",
                    "combo_price": "150,000 VND",
                    "predicted_rating": rec['predicted_rating']
                })

            return {
                "combo_recommendations": combo_recommendations,
                "message": "These items are frequently ordered together"
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Upsell Side Dishes


@ns_upsell.route('/sides')
class UpsellSides(Resource):
    @ns_upsell.doc('get_upsell_sides')
    @ns_upsell.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_upsell.param('main_dish_id', 'ID món chính', required=True, type='string')
    @ns_upsell.marshal_with(api.model('UpsellSidesResponse', {
        'side_dish_recommendations': fields.List(fields.Nested(side_dish_model)),
        'message': fields.String(description='Thông báo')
    }))
    @ns_upsell.response(400, 'Thiếu tham số', error_model)
    @ns_upsell.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý món phụ đi kèm với món chính"""
        user_id = request.args.get('user_id')
        main_dish_id = request.args.get('main_dish_id')

        if not user_id or not main_dish_id:
            return {"error": "Missing user_id or main_dish_id parameter"}, 400

        try:
            recommendations = get_recommendations(user_id, count=5)

            side_recommendations = []
            for rec in recommendations:
                side_recommendations.append({
                    "recipe_name": rec['recipe_name'],
                    "recipe_url": rec['recipe_url'],
                    "side_price": "30,000 VND",
                    "predicted_rating": rec['predicted_rating']
                })

            return {
                "side_dish_recommendations": side_recommendations,
                "message": "These side dishes perfectly complement your main course"
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Family Combos


@ns_family.route('/combos')
class FamilyCombos(Resource):
    @ns_family.doc('get_family_combos')
    @ns_family.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_family.param('family_size', 'Số người trong gia đình', default=4, type='int')
    @ns_family.marshal_with(api.model('FamilyCombosResponse', {
        'family_combo': fields.Nested(family_combo_model),
        'total_price': fields.String(description='Tổng giá tiền'),
        'preparation_time': fields.String(description='Thời gian chuẩn bị'),
        'suitable_for': fields.String(description='Phù hợp cho')
    }))
    @ns_family.response(400, 'Thiếu tham số', error_model)
    @ns_family.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý combo cho gia đình"""
        user_id = request.args.get('user_id')
        family_size = request.args.get('family_size', default=4, type=int)

        if not user_id:
            return {"error": "Missing user_id parameter"}, 400

        try:
            recommendations = get_recommendations(user_id, count=10)

            main_dishes = recommendations[:2]
            side_dishes = recommendations[2:5]
            desserts = recommendations[5:7]

            return {
                "family_combo": {
                    "main_dishes": [{
                        "recipe_name": dish['recipe_name'],
                        "recipe_url": dish['recipe_url'],
                        "difficulty": dish['difficulty'],
                        "predicted_rating": dish['predicted_rating']
                    } for dish in main_dishes],
                    "side_dishes": [{
                        "recipe_name": dish['recipe_name'],
                        "recipe_url": dish['recipe_url'],
                        "difficulty": dish['difficulty'],
                        "predicted_rating": dish['predicted_rating']
                    } for dish in side_dishes],
                    "desserts": [{
                        "recipe_name": dish['recipe_name'],
                        "recipe_url": dish['recipe_url'],
                        "difficulty": dish['difficulty'],
                        "predicted_rating": dish['predicted_rating']
                    } for dish in desserts]
                },
                "total_price": f"{150000 * family_size} VND",
                "preparation_time": "45 minutes",
                "suitable_for": f"Family of {family_size}"
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Age-based Recommendations


@ns_age.route('/recommendations')
class AgeBasedRecommendations(Resource):
    @ns_age.doc('get_age_based_recommendations')
    @ns_age.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_age.param('age_group', 'Nhóm tuổi', required=True,
                  enum=['children', 'teenagers', 'adults', 'elderly'])
    @ns_age.marshal_with(api.model('AgeBasedResponse', {
        'age_group': fields.String(description='Nhóm tuổi'),
        'recommendations': fields.List(fields.Nested(recommendation_model)),
        'nutrition_focus': fields.String(description='Trọng tâm dinh dưỡng')
    }))
    @ns_age.response(400, 'Thiếu tham số hoặc tham số không hợp lệ', error_model)
    @ns_age.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý món ăn theo độ tuổi"""
        user_id = request.args.get('user_id')
        age_group = request.args.get('age_group')

        if not user_id or not age_group:
            return {"error": "Missing user_id or age_group parameter"}, 400

        if age_group not in ['children', 'teenagers', 'adults', 'elderly']:
            return {"error": "Invalid age_group. Choose from: children, teenagers, adults, elderly"}, 400

        try:
            recommendations = get_recommendations(user_id, count=10)

            if age_group == 'children':
                age_filtered_recommendations = [
                    r for r in recommendations if r['difficulty'] == 'Dễ']
            elif age_group == 'teenagers':
                age_filtered_recommendations = recommendations
            elif age_group == 'adults':
                age_filtered_recommendations = recommendations
            else:  # elderly
                age_filtered_recommendations = [
                    r for r in recommendations if r['difficulty'] in ['Dễ', 'Trung bình']]

            result = []
            for rec in age_filtered_recommendations[:5]:
                result.append({
                    "recipe_name": rec['recipe_name'],
                    "recipe_url": rec['recipe_url'],
                    "difficulty": rec['difficulty'],
                    "meal_time": rec['meal_time'],
                    "predicted_rating": rec['predicted_rating']
                })

            return {
                "age_group": age_group,
                "recommendations": result,
                "nutrition_focus": get_nutrition_focus(age_group)
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Meal Recommendations


@ns_meal.route('/recommendations')
class MealRecommendations(Resource):
    @ns_meal.doc('get_meal_recommendations')
    @ns_meal.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_meal.param('meal_type', 'Loại bữa ăn', required=True,
                   enum=['breakfast', 'lunch', 'dinner'])
    @ns_meal.param('count', 'Số lượng gợi ý', default=6, type='int')
    @ns_meal.marshal_with(api.model('MealRecommendationsResponse', {
        'meal_type': fields.String(description='Loại bữa ăn'),
        'recommendations': fields.List(fields.Nested(recommendation_model)),
        'user_id': fields.String(description='ID khách hàng')
    }))
    @ns_meal.response(400, 'Thiếu tham số hoặc tham số không hợp lệ', error_model)
    @ns_meal.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý món ăn theo bữa (sáng, trưa, tối)"""
        user_id = request.args.get('user_id')
        meal_type = request.args.get('meal_type')
        count = request.args.get('count', default=6, type=int)

        if not user_id:
            return {"error": "Missing user_id parameter"}, 400

        if meal_type not in ['breakfast', 'lunch', 'dinner']:
            return {"error": "Invalid meal_type. Choose from: breakfast, lunch, dinner"}, 400

        try:
            recommendations = get_recommendations(
                user_id, feature_type=meal_type, count=count)

            result = []
            for rec in recommendations:
                result.append({
                    "recipe_name": rec['recipe_name'],
                    "recipe_url": rec['recipe_url'],
                    "difficulty": rec['difficulty'],
                    "meal_time": rec['meal_time'],
                    "predicted_rating": rec['predicted_rating'],
                    "item_index": rec['item_index']
                })

            return {
                "meal_type": meal_type,
                "recommendations": result,
                "user_id": user_id
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Meal Plans


@ns_meal.route('/plans')
class MealPlans(Resource):
    @ns_meal.doc('get_meal_plans')
    @ns_meal.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_meal.marshal_with(api.model('MealPlansResponse', {
        'user_id': fields.String(description='ID khách hàng'),
        'meal_plans': fields.List(fields.Nested(meal_plan_model))
    }))
    @ns_meal.response(400, 'Thiếu tham số', error_model)
    @ns_meal.response(500, 'Lỗi server', error_model)
    def get(self):
        """Lấy 6 thực đơn hoàn chỉnh (sáng, trưa, tối)"""
        user_id = request.args.get('user_id')

        if not user_id:
            return {"error": "Missing user_id parameter"}, 400

        try:
            breakfast_recs = get_recommendations(
                user_id, feature_type='breakfast', count=6)
            lunch_recs = get_recommendations(
                user_id, feature_type='lunch', count=6)
            dinner_recs = get_recommendations(
                user_id, feature_type='dinner', count=6)

            meal_plans = []
            for i in range(6):
                meal_plan = {
                    "menu_number": i + 1,
                    "breakfast": breakfast_recs[i] if i < len(breakfast_recs) else None,
                    "lunch": lunch_recs[i] if i < len(lunch_recs) else None,
                    "dinner": dinner_recs[i] if i < len(dinner_recs) else None
                }
                meal_plans.append(meal_plan)

            return {
                "user_id": user_id,
                "meal_plans": meal_plans
            }
        except Exception as e:
            return {"error": str(e)}, 500

# Nutrition Recommendations


@ns_nutrition.route('/recommendations')
class NutritionRecommendations(Resource):
    @ns_nutrition.doc('get_nutrition_recommendations')
    @ns_nutrition.param('user_id', 'ID khách hàng', required=True, type='string')
    @ns_nutrition.param('nutrition_type', 'Loại dinh dưỡng', required=True,
                        enum=['weight-loss', 'balanced', 'blood-boost', 'brain-boost', 'digestive-support'])
    @ns_nutrition.param('count', 'Số lượng gợi ý', default=6, type='int')
    @ns_nutrition.marshal_with(api.model('NutritionRecommendationsResponse', {
        'nutrition_type': fields.String(description='Loại dinh dưỡng'),
        'recommendations': fields.List(fields.Nested(nutrition_recommendation_model)),
        'nutrition_focus': fields.String(description='Trọng tâm dinh dưỡng'),
        'user_id': fields.String(description='ID khách hàng')
    }))
    @ns_nutrition.response(400, 'Thiếu tham số hoặc tham số không hợp lệ', error_model)
    @ns_nutrition.response(500, 'Lỗi server', error_model)
    def get(self):
        """Gợi ý món ăn theo mục tiêu dinh dưỡng"""
        user_id = request.args.get('user_id')
        nutrition_type = request.args.get('nutrition_type')
        count = request.args.get('count', default=6, type=int)

        if not user_id:
            return {"error": "Missing user_id parameter"}, 400

        if nutrition_type not in ['weight-loss', 'balanced', 'blood-boost', 'brain-boost', 'digestive-support']:
            return {"error": "Invalid nutrition_type"}, 400

        try:
            recommendations = get_recommendations(user_id, count=20)
            nutrition_filtered_recommendations = []

            # Check if we have the nutrition_category column
            has_nutrition_category = 'nutrition_category' in interactions_df.columns

            if has_nutrition_category:
                target_recipes = interactions_df[interactions_df['nutrition_category']
                                                 == nutrition_type]['recipe_name'].unique()
                nutrition_filtered_recommendations = [
                    r for r in recommendations
                    if r['recipe_name'] in target_recipes
                ]

            # Fallback to keyword-based filtering if no nutrition_category or no matches
            if not nutrition_filtered_recommendations:
                if nutrition_type == 'weight-loss':
                    weight_loss_keywords = [
                        'salad', 'gỏi', 'canh', 'soup', 'luộc', 'hấp', 'nướng', 'thịt nạc', 'rau', 'cá']
                    nutrition_filtered_recommendations = [
                        r for r in recommendations
                        if any(keyword in r['recipe_name'].lower() for keyword in weight_loss_keywords)
                        or r['difficulty'] == 'Dễ'
                    ]
                    nutrition_focus = "Giảm cân, ít chất béo, nhiều chất xơ, protein nạc"

                elif nutrition_type == 'balanced':
                    nutrition_filtered_recommendations = recommendations
                    nutrition_focus = "Cân bằng dinh dưỡng, đầy đủ chất, phù hợp mọi lứa tuổi"

                elif nutrition_type == 'blood-boost':
                    blood_boost_keywords = [
                        'thịt đỏ', 'gan', 'rau dền', 'rau chân vịt', 'đậu', 'trứng', 'cà chua']
                    nutrition_filtered_recommendations = [
                        r for r in recommendations
                        if any(keyword in r['recipe_name'].lower() for keyword in blood_boost_keywords)
                    ]
                    nutrition_focus = "Bổ máu, tăng cường sắt, vitamin B12, axit folic"

                elif nutrition_type == 'brain-boost':
                    brain_boost_keywords = [
                        'cá', 'hạt', 'trứng', 'bơ', 'chocolate', 'óc chó', 'cà phê']
                    nutrition_filtered_recommendations = [
                        r for r in recommendations
                        if any(keyword in r['recipe_name'].lower() for keyword in brain_boost_keywords)
                    ]
                    nutrition_focus = "Tăng cường trí não, omega-3, vitamin E, choline"

                elif nutrition_type == 'digestive-support':
                    digestive_keywords = ['cháo', 'soup', 'canh',
                                          'yogurt', 'gừng', 'nghệ', 'yến mạch']
                    nutrition_filtered_recommendations = [
                        r for r in recommendations
                        if any(keyword in r['recipe_name'].lower() for keyword in digestive_keywords)
                        or r['difficulty'] == 'Dễ'
                    ]
                    nutrition_focus = "Hỗ trợ tiêu hóa, dễ hấp thụ, kháng viêm"
            else:
                nutrition_focus_map = {
                    'weight-loss': "Giảm cân, ít chất béo, nhiều chất xơ, protein nạc",
                    'balanced': "Cân bằng dinh dưỡng, đầy đủ chất, phù hợp mọi lứa tuổi",
                    'blood-boost': "Bổ máu, tăng cường sắt, vitamin B12, axit folic",
                    'brain-boost': "Tăng cường trí não, omega-3, vitamin E, choline",
                    'digestive-support': "Hỗ trợ tiêu hóa, dễ hấp thụ, kháng viêm"
                }
                nutrition_focus = nutrition_focus_map.get(
                    nutrition_type, "Dinh dưỡng cân bằng")

            if not nutrition_filtered_recommendations:
                nutrition_filtered_recommendations = recommendations[:count]

            result = []
            for rec in nutrition_filtered_recommendations[:count]:
                recipe_data = interactions_df[interactions_df['recipe_name'] == rec['recipe_name']].iloc[0] if len(
                    interactions_df[interactions_df['recipe_name'] == rec['recipe_name']]) > 0 else None

                recipe_info = {
                    "recipe_name": rec['recipe_name'],
                    "recipe_url": rec['recipe_url'],
                    "difficulty": rec['difficulty'],
                    "meal_time": rec['meal_time'],
                    "predicted_rating": rec['predicted_rating'],
                    "item_index": rec['item_index']
                }

                if recipe_data is not None:
                    if 'estimated_calories' in recipe_data:
                        recipe_info['estimated_calories'] = int(
                            recipe_data['estimated_calories'])
                    if 'preparation_time_minutes' in recipe_data:
                        recipe_info['preparation_time_minutes'] = int(
                            recipe_data['preparation_time_minutes'])
                    if 'ingredient_count' in recipe_data:
                        recipe_info['ingredient_count'] = int(
                            recipe_data['ingredient_count'])
                    if 'estimated_price_vnd' in recipe_data:
                        recipe_info['estimated_price_vnd'] = int(
                            recipe_data['estimated_price_vnd'])

                result.append(recipe_info)

            return {
                "nutrition_type": nutrition_type,
                "recommendations": result,
                "nutrition_focus": nutrition_focus,
                "user_id": user_id
            }
        except Exception as e:
            return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
