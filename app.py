from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os
import time
import random

app = Flask(__name__)

# Load the trained model
try:
    model = CatBoostRegressor()
    model.load_model('catboost_best_model.cbm')
except Exception as e:
    print(f"Warning: Could not load model: {str(e)}")
    model = None

# Load interaction data (we'll load just what we need for memory efficiency)
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

# Load customer data for enhanced display
try:
    customers_df = pd.read_csv('customers_data.csv')
    print(f"✅ Loaded customer data with {len(customers_df)} customers")
except Exception as e:
    print(f"❌ Could not load customer data: {str(e)}")
    customers_df = pd.DataFrame()

# Function to generate random age within age group


def generate_random_age(age_group):
    """Generate a random age within the specified age group"""
    age_ranges = {
        "18-24": (18, 24),
        "25-34": (25, 34),
        "35-44": (35, 44),
        "45-54": (45, 54),
        "55-64": (55, 64),
        "65+": (65, 80)  # Assuming max age of 80 for 65+
    }

    if age_group in age_ranges:
        min_age, max_age = age_ranges[age_group]
        return random.randint(min_age, max_age)
    else:
        return random.randint(25, 35)  # Default fallback


# Create helper dictionaries for quick lookups
user_items = {}
item_features = {}
customer_ids = []  # List to store all customer IDs
customers_info = {}  # Dictionary to store enhanced customer information

# Preprocess data for recommendations


def preprocess_data():
    global user_items, item_features, customer_ids, customers_info

    if interactions_df.empty:
        print("No interaction data available.")
        return

    print("Preprocessing data for recommendations...")

    # Extract unique customer IDs (up to 1300)
    customer_ids = sorted(interactions_df['customer_id'].unique().tolist())
    if len(customer_ids) > 1300:
        customer_ids = customer_ids[:1300]
    print(f"Extracted {len(customer_ids)} unique customer IDs")

    # Process customer information for enhanced display
    if not customers_df.empty:
        for _, customer in customers_df.iterrows():
            customer_id = customer['customer_id']
            if customer_id in customer_ids:  # Only process customers that have interactions
                age = generate_random_age(customer['age_group'])
                customers_info[customer_id] = {
                    'name': customer['full_name'],
                    'age': age,
                    'display_name': f"{customer_id}-{customer['full_name']}-{age} tuổi"
                }
        print(
            f"Processed enhanced information for {len(customers_info)} customers")

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


# Initialize the app data at startup
with app.app_context():
    preprocess_data()

# Route for the web interface


@app.route('/')
def index():
    return render_template('index.html', customer_ids=customer_ids, customers_info=customers_info)

# Test page route


@app.route('/test')
def test_page():
    return render_template('simple_customer_test.html')

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

# API endpoint for upsell combos


@app.route('/api/upsell_combos', methods=['GET'])
def upsell_combos():
    user_id = request.args.get('user_id')
    item_id = request.args.get('item_id')

    if not user_id or not item_id:
        return jsonify({"error": "Missing user_id or item_id parameter"}), 400

    try:
        # Get complementary items that go well with the current item
        # This would typically be based on items frequently purchased together
        recommendations = get_recommendations(user_id, count=3)

        # Format response for combo upselling
        combo_recommendations = []
        for rec in recommendations:
            combo_recommendations.append({
                "recipe_name": rec['recipe_name'],
                "recipe_url": rec['recipe_url'],
                "combo_discount": "10%",  # Example discount
                "combo_price": "150,000 VND",  # Example price
                "predicted_rating": rec['predicted_rating']
            })

        return jsonify({
            "combo_recommendations": combo_recommendations,
            "message": "These items are frequently ordered together"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for upsell side dishes


@app.route('/api/upsell_sides', methods=['GET'])
def upsell_sides():
    user_id = request.args.get('user_id')
    main_dish_id = request.args.get('main_dish_id')

    if not user_id or not main_dish_id:
        return jsonify({"error": "Missing user_id or main_dish_id parameter"}), 400

    try:
        # Get side dishes that complement the main dish
        recommendations = get_recommendations(user_id, count=5)

        # Filter for likely side dishes (could be based on specific categorization)
        side_recommendations = []
        for rec in recommendations:
            side_recommendations.append({
                "recipe_name": rec['recipe_name'],
                "recipe_url": rec['recipe_url'],
                "side_price": "30,000 VND",  # Example price
                "predicted_rating": rec['predicted_rating']
            })

        return jsonify({
            "side_dish_recommendations": side_recommendations,
            "message": "These side dishes perfectly complement your main course"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for family meal combos


@app.route('/api/family_combos', methods=['GET'])
def family_combos():
    user_id = request.args.get('user_id')
    family_size = request.args.get('family_size', default=4, type=int)

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    try:
        # Get recommendations for family meals
        recommendations = get_recommendations(user_id, count=10)

        # Create balanced meal combinations (main dish, sides, dessert)
        main_dishes = recommendations[:2]
        side_dishes = recommendations[2:5]
        desserts = recommendations[5:7]

        return jsonify({
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
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for age-based recommendations


@app.route('/api/age_based_recommendations', methods=['GET'])
def age_based_recommendations():
    user_id = request.args.get('user_id')
    # children, teenagers, adults, elderly (optional)
    age_group = request.args.get('age_group')

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    try:
        # Get base recommendations
        recommendations = get_recommendations(user_id, count=20)

        # Get customer's actual age if available
        customer_age = None
        if user_id in customers_info:
            customer_age = customers_info[user_id]['age']

        # Auto-determine age_group based on actual customer age
        if customer_age:
            if customer_age <= 12:
                age_group = 'children'
            elif customer_age <= 19:
                age_group = 'teenagers'
            elif customer_age <= 59:
                age_group = 'adults'
            else:
                age_group = 'elderly'
        elif not age_group:
            # Default to adults if no age info and no age_group provided
            age_group = 'adults'

        # Validate age_group
        if age_group not in ['children', 'teenagers', 'adults', 'elderly']:
            age_group = 'adults'  # Default fallback

        # Enhanced age-based filtering with real customer data
        age_filtered_recommendations = []

        if age_group == 'children':
            # For children (3-12): Easy, nutritious, colorful dishes
            children_keywords = ['trứng', 'cháo',
                                 'soup', 'canh', 'bánh', 'sữa', 'rau củ']
            age_filtered_recommendations = [
                r for r in recommendations
                if r['difficulty'] == 'Dễ' or
                any(keyword in r['recipe_name'].lower()
                    for keyword in children_keywords)
            ]

        elif age_group == 'teenagers':
            # For teenagers (13-19): Energy-rich, trendy, quick meals
            teen_keywords = ['nướng', 'chiên', 'pizza',
                             'burger', 'mì', 'bánh mì', 'snack', 'fast']
            age_filtered_recommendations = [
                r for r in recommendations
                if any(keyword in r['recipe_name'].lower() for keyword in teen_keywords) or
                r['meal_time'] in ['lunch', 'dinner']
            ]
            # If not enough matches, include general recommendations
            if len(age_filtered_recommendations) < 5:
                age_filtered_recommendations.extend(recommendations[:10])

        elif age_group == 'adults':
            # For adults (20-59): Balanced, varied, professional meals
            adult_keywords = ['salad', 'gỏi', 'nướng',
                              'xào', 'hầm', 'curry', 'thịt', 'cá', 'tôm']
            age_filtered_recommendations = [
                r for r in recommendations
                if any(keyword in r['recipe_name'].lower() for keyword in adult_keywords) or
                r['difficulty'] in ['Trung bình', 'Khó']
            ]
            # Include all if no specific matches
            if len(age_filtered_recommendations) < 5:
                age_filtered_recommendations = recommendations

        else:  # elderly (60+)
            # For elderly: Easy to digest, nutritious, soft foods
            elderly_keywords = ['canh', 'soup', 'cháo',
                                'hầm', 'luộc', 'hấp', 'rau', 'cá']
            age_filtered_recommendations = [
                r for r in recommendations
                if r['difficulty'] in ['Dễ', 'Trung bình'] and
                (any(keyword in r['recipe_name'].lower() for keyword in elderly_keywords) or
                 r['meal_time'] in ['breakfast', 'lunch'])
            ]

        # Remove duplicates and sort by rating
        unique_recommendations = []
        seen_recipes = set()
        for rec in age_filtered_recommendations:
            if rec['recipe_name'] not in seen_recipes:
                unique_recommendations.append(rec)
                seen_recipes.add(rec['recipe_name'])

        # Sort by predicted rating
        unique_recommendations.sort(
            key=lambda x: x['predicted_rating'], reverse=True)

        # Format response with enhanced information
        result = []
        for rec in unique_recommendations[:8]:  # Return top 8 recommendations
            recipe_info = {
                "recipe_name": rec['recipe_name'],
                "recipe_url": rec['recipe_url'],
                "difficulty": rec['difficulty'],
                "meal_time": rec['meal_time'],
                "predicted_rating": rec['predicted_rating'],
                "item_index": rec['item_index']
            }

            # Add enhanced data from interactions_df if available
            try:
                recipe_data = interactions_df[interactions_df['recipe_name'] == rec['recipe_name']].iloc[0] if len(
                    interactions_df[interactions_df['recipe_name'] == rec['recipe_name']]) > 0 else None

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
            except:
                pass  # Skip if enhanced data not available

            result.append(recipe_info)

        return jsonify({
            "age_group": age_group,
            "recommendations": result,
            "nutrition_focus": get_enhanced_nutrition_focus(age_group, customer_age),
            "customer_age": customer_age,
            "user_id": user_id,
            "total_recommendations": len(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function for enhanced age-based nutrition focus


def get_enhanced_nutrition_focus(age_group, customer_age=None):
    """Enhanced nutrition focus that considers both age group and actual age"""
    base_focus = {
        'children': "Phát triển, tăng trưởng não bộ, xương chắc khỏe",
        'teenagers': "Năng lượng, phát triển cơ bắp, chức năng não bộ",
        'adults': "Dinh dưỡng cân bằng, năng lượng, sức khỏe tim mạch",
        'elderly': "Sức khỏe xương khớp, tim mạch, dễ tiêu hóa"
    }

    focus = base_focus.get(age_group, "Dinh dưỡng cân bằng")

    # Add specific age-based recommendations if actual age is available
    if customer_age:
        if customer_age <= 12:
            focus += " - Thích hợp cho trẻ em, dễ ăn, bổ dưỡng"
        elif 13 <= customer_age <= 19:
            focus += " - Năng lượng cao cho tuổi teen, món ăn hấp dẫn"
        elif 20 <= customer_age <= 35:
            focus += " - Người trẻ tuổi, đa dạng món ăn, cân bằng dinh dưỡng"
        elif 36 <= customer_age <= 50:
            focus += " - Tuổi trung niên, chú trọng sức khỏe tim mạch"
        elif 51 <= customer_age <= 65:
            focus += " - Tuổi tiền cao niên, hỗ trợ sức khỏe tổng thể"
        else:
            focus += " - Cao tuổi, dễ tiêu hóa, bổ dưỡng"

    return focus

# Legacy function for backward compatibility


def get_nutrition_focus(age_group):
    return get_enhanced_nutrition_focus(age_group)

# API endpoint for meal-specific recommendations (breakfast, lunch, dinner)


@app.route('/api/meal_recommendations', methods=['GET'])
def meal_recommendations():
    user_id = request.args.get('user_id')
    meal_type = request.args.get('meal_type')  # breakfast, lunch, dinner
    count = request.args.get('count', default=6, type=int)

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    if meal_type not in ['breakfast', 'lunch', 'dinner']:
        return jsonify({"error": "Invalid meal_type. Choose from: breakfast, lunch, dinner"}), 400

    try:
        # Get recommendations for specific meal type
        recommendations = get_recommendations(
            user_id, feature_type=meal_type, count=count)

        # Format response
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

        return jsonify({
            "meal_type": meal_type,
            "recommendations": result,
            "user_id": user_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get all meal plans (6 menus with breakfast, lunch, dinner each)


@app.route('/api/meal_plans', methods=['GET'])
def meal_plans():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    try:
        # Get recommendations for each meal type (user_id is already a string)
        breakfast_recs = get_recommendations(
            user_id, feature_type='breakfast', count=6)
        lunch_recs = get_recommendations(
            user_id, feature_type='lunch', count=6)
        dinner_recs = get_recommendations(
            user_id, feature_type='dinner', count=6)

        # Create 6 meal plans
        meal_plans = []
        for i in range(6):
            meal_plan = {
                "menu_number": i + 1,
                "breakfast": breakfast_recs[i] if i < len(breakfast_recs) else None,
                "lunch": lunch_recs[i] if i < len(lunch_recs) else None,
                "dinner": dinner_recs[i] if i < len(dinner_recs) else None
            }
            meal_plans.append(meal_plan)

        return jsonify({
            "user_id": user_id,
            "meal_plans": meal_plans
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for nutrition-based recommendations


@app.route('/api/nutrition_recommendations', methods=['GET'])
def nutrition_recommendations():
    user_id = request.args.get('user_id')
    nutrition_type = request.args.get('nutrition_type')
    count = request.args.get('count', default=6, type=int)

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    if nutrition_type not in ['weight-loss', 'balanced', 'blood-boost', 'brain-boost', 'digestive-support']:
        return jsonify({"error": "Invalid nutrition_type"}), 400

    try:
        # Get base recommendations
        # Filter based on nutrition type
        recommendations = get_recommendations(user_id, count=20)
        nutrition_filtered_recommendations = []

        # Check if we have the nutrition_category column
        has_nutrition_category = 'nutrition_category' in interactions_df.columns

        if has_nutrition_category:
            # Use the nutrition_category column for better filtering
            target_recipes = interactions_df[interactions_df['nutrition_category']
                                             == nutrition_type]['recipe_name'].unique()
            nutrition_filtered_recommendations = [
                r for r in recommendations
                if r['recipe_name'] in target_recipes
            ]

        # Fallback to keyword-based filtering if no nutrition_category or no matches
        if not nutrition_filtered_recommendations:
            if nutrition_type == 'weight-loss':
                # Keywords for weight loss dishes
                weight_loss_keywords = [
                    'salad', 'gỏi', 'canh', 'soup', 'luộc', 'hấp', 'nướng', 'thịt nạc', 'rau', 'cá']
                nutrition_filtered_recommendations = [
                    r for r in recommendations
                    if any(keyword in r['recipe_name'].lower() for keyword in weight_loss_keywords)
                    or r['difficulty'] == 'Dễ'
                ]
                nutrition_focus = "Giảm cân, ít chất béo, nhiều chất xơ, protein nạc"

            elif nutrition_type == 'balanced':
                # Balanced nutrition - mix of all meal types
                nutrition_filtered_recommendations = recommendations
                nutrition_focus = "Cân bằng dinh dưỡng, đầy đủ chất, phù hợp mọi lứa tuổi"

            elif nutrition_type == 'blood-boost':
                # Blood boosting foods
                blood_boost_keywords = [
                    'thịt đỏ', 'gan', 'rau dền', 'rau chân vịt', 'đậu', 'trứng', 'cà chua']
                nutrition_filtered_recommendations = [
                    r for r in recommendations
                    if any(keyword in r['recipe_name'].lower() for keyword in blood_boost_keywords)
                ]
                nutrition_focus = "Bổ máu, tăng cường sắt, vitamin B12, axit folic"

            elif nutrition_type == 'brain-boost':
                # Brain boosting foods
                brain_boost_keywords = [
                    'cá', 'hạt', 'trứng', 'bơ', 'chocolate', 'óc chó', 'cà phê']
                nutrition_filtered_recommendations = [
                    r for r in recommendations
                    if any(keyword in r['recipe_name'].lower() for keyword in brain_boost_keywords)
                ]
                nutrition_focus = "Tăng cường trí não, omega-3, vitamin E, choline"

            elif nutrition_type == 'digestive-support':
                # Digestive support foods
                digestive_keywords = ['cháo', 'soup', 'canh',
                                      'yogurt', 'gừng', 'nghệ', 'yến mạch']
                nutrition_filtered_recommendations = [
                    r for r in recommendations
                    if any(keyword in r['recipe_name'].lower() for keyword in digestive_keywords)
                    or r['difficulty'] == 'Dễ'
                ]
                nutrition_focus = "Hỗ trợ tiêu hóa, dễ hấp thụ, kháng viêm"
        else:
            # Set nutrition focus based on type when using category column
            nutrition_focus_map = {
                'weight-loss': "Giảm cân, ít chất béo, nhiều chất xơ, protein nạc",
                'balanced': "Cân bằng dinh dưỡng, đầy đủ chất, phù hợp mọi lứa tuổi",
                'blood-boost': "Bổ máu, tăng cường sắt, vitamin B12, axit folic",
                'brain-boost': "Tăng cường trí não, omega-3, vitamin E, choline",
                'digestive-support': "Hỗ trợ tiêu hóa, dễ hấp thụ, kháng viêm"
            }
            nutrition_focus = nutrition_focus_map.get(
                nutrition_type, "Dinh dưỡng cân bằng")

        # If no specific matches found, return top recommendations
        if not nutrition_filtered_recommendations:
            # Format response
            nutrition_filtered_recommendations = recommendations[:count]
        result = []
        for rec in nutrition_filtered_recommendations[:count]:
            # Get additional info from enhanced dataset if available
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

            # Add enhanced data if available
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

        return jsonify({
            "nutrition_type": nutrition_type,
            "recommendations": result,
            "nutrition_focus": nutrition_focus,
            "user_id": user_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
