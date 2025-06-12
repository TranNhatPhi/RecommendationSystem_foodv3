import pandas as pd
import sqlite3

print("🔍 Checking data loading status...")

# Check CSV file
print("\n1. CSV File Status:")
try:
    df = pd.read_csv('interactions_enhanced_final.csv')
    print(f"   ✅ Total interactions in CSV: {len(df):,}")
    print(f"   ✅ Unique recipes: {df['recipe_name'].nunique()}")
    print(f"   ✅ Unique customers: {df['customer_id'].nunique()}")
    print(
        f"   ✅ Date range: {df['interaction_date'].min()} to {df['interaction_date'].max()}")
except Exception as e:
    print(f"   ❌ Error reading CSV: {e}")

# Check SQLite database
print("\n2. SQLite Database Status:")
try:
    conn = sqlite3.connect('simple_food_db.sqlite')
    cursor = conn.cursor()

    # Check recipes table
    cursor.execute("SELECT COUNT(*) FROM recipes")
    recipes_count = cursor.fetchone()[0]
    print(f"   ✅ Recipes in database: {recipes_count}")

    # Check customers table
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count = cursor.fetchone()[0]
    print(f"   ✅ Customers in database: {customers_count}")

    # Check search keywords
    cursor.execute("SELECT COUNT(*) FROM search_keywords")
    keywords_count = cursor.fetchone()[0]
    print(f"   ✅ Search keywords: {keywords_count}")

    # Sample some data
    cursor.execute(
        "SELECT recipe_name, estimated_calories, avg_rating FROM recipes LIMIT 5")
    sample_recipes = cursor.fetchall()
    print(f"\n   📋 Sample recipes:")
    for recipe in sample_recipes:
        print(f"      - {recipe[0]} ({recipe[1]} cal, {recipe[2]:.1f}⭐)")

    conn.close()

except Exception as e:
    print(f"   ❌ Error reading database: {e}")

# Check if database is properly populated
print("\n3. Data Integration Check:")
try:
    from simple_food_db import SimpleFoodRecommendationDB

    db = SimpleFoodRecommendationDB()
    stats = db.get_collection_stats()

    print(f"   ✅ Vector DB recipes: {stats['recipes_count']}")
    print(f"   ✅ Vector DB customers: {stats['customers_count']}")

    # Test search functionality
    search_result = db.search_recipes("món ăn healthy", n_results=3)
    if search_result and search_result['documents']:
        print(
            f"   ✅ Search functionality working: {len(search_result['documents'][0])} results")
    else:
        print("   ⚠️ Search functionality issue")

except Exception as e:
    print(f"   ❌ Error with vector database: {e}")

print("\n4. App Loading Check:")
try:
    # Check app.py loading
    import pandas as pd

    # Simulate app loading
    interactions_df = pd.read_csv('interactions_enhanced_final.csv')
    customers_df = pd.read_csv('customers_data.csv')

    print(f"   ✅ App can load interactions: {len(interactions_df):,} rows")
    print(f"   ✅ App can load customers: {len(customers_df):,} rows")

    # Check unique customer IDs extraction
    customer_ids = interactions_df['customer_id'].unique()
    print(f"   ✅ Unique customer IDs extracted: {len(customer_ids)}")

except Exception as e:
    print(f"   ❌ Error simulating app loading: {e}")

print("\n📊 Summary:")
print("=" * 50)
if 'df' in locals() and 'recipes_count' in locals():
    print(f"CSV Interactions: {len(df):,}")
    print(f"DB Recipes: {recipes_count}")
    print(f"DB Customers: {customers_count}")

    if len(df) > 10000 and recipes_count > 50:
        print("🎉 Status: ✅ DATA FULLY LOADED")
    else:
        print("⚠️ Status: PARTIAL DATA LOADING")
else:
    print("❌ Status: DATA LOADING ISSUES")
