from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os
import time

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
    interactions_df = pd.read_csv('interactions_encoded.csv')
except Exception as e:
    print(f"Warning: Could not load interactions data: {str(e)}")
    interactions_df = pd.DataFrame()

# Create helper dictionaries for quick lookups
user_items = {}
item_features = {}
customer_ids = []  # List to store all customer IDs

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


# Initialize the app data at startup
with app.app_context():
    preprocess_data()

# Route for the web interface


@app.route('/')
def index():
    return render_template('index.html', customer_ids=customer_ids)

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
        # For demo purposes, if model is not available, use the precomputed scores
        if model is None:
            prediction = item_features[item_index].get(
                'cf_score', 0) + item_features[item_index].get('content_score', 0)
        else:
            # Prepare features for prediction
            try:
                features = {
                    'user_index': [list(user_items.keys()).index(user_id)],
                    'item_index': [item_index],
                    # Add more features as needed based on the model requirements
                }

                # Make prediction
                prediction = model.predict(features)[0]
            except Exception as e:
                print(f"Error predicting for item {item_index}: {str(e)}")
                prediction = item_features[item_index].get(
                    'cf_score', 0) + item_features[item_index].get('content_score', 0)

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
    # children, teenagers, adults, elderly
    age_group = request.args.get('age_group')

    if not user_id or not age_group:
        return jsonify({"error": "Missing user_id or age_group parameter"}), 400

    if age_group not in ['children', 'teenagers', 'adults', 'elderly']:
        return jsonify({"error": "Invalid age_group. Choose from: children, teenagers, adults, elderly"}), 400

    try:
        # Get base recommendations
        recommendations = get_recommendations(user_id, count=10)

        # Filter and sort based on age group preferences
        if age_group == 'children':
            # For children: easier recipes, potentially sweeter, nutritious
            age_filtered_recommendations = [
                r for r in recommendations if r['difficulty'] == 'Dễ']
        elif age_group == 'teenagers':
            # For teenagers: mix of preferences, potentially more snacks
            age_filtered_recommendations = recommendations
        elif age_group == 'adults':
            # For adults: all types of recipes
            age_filtered_recommendations = recommendations
        else:  # elderly
            # For elderly: potentially softer foods, nutritious, easier to digest
            age_filtered_recommendations = [
                r for r in recommendations if r['difficulty'] in ['Dễ', 'Trung bình']]

        # Format response
        result = []
        for rec in age_filtered_recommendations[:5]:
            result.append({
                "recipe_name": rec['recipe_name'],
                "recipe_url": rec['recipe_url'],
                "difficulty": rec['difficulty'],
                "meal_time": rec['meal_time'],
                "predicted_rating": rec['predicted_rating']
            })

        return jsonify({
            "age_group": age_group,
            "recommendations": result,
            "nutrition_focus": get_nutrition_focus(age_group)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
