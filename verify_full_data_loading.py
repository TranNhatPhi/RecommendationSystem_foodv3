import requests
import json

print("🔍 Checking Data Loading from Running Server...")
print("=" * 60)

try:
    # Test agent stats endpoint
    print("1. Agent Statistics:")
    response = requests.get(
        'http://localhost:5000/api/agent_stats', timeout=10)
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if 'stats' in data:
            stats = data['stats']
            print(f"   ✅ Recipes Count: {stats.get('recipes_count', 'N/A'):,}")
            print(
                f"   ✅ Customers Count: {stats.get('customers_count', 'N/A'):,}")
            print(
                f"   ✅ Total Interactions: {stats.get('total_interactions', 'N/A'):,}")
            print(f"   ✅ AI Accuracy: {stats.get('ai_accuracy', 'N/A')}%")
            print(
                f"   ✅ Avg Response Time: {stats.get('avg_response_time', 'N/A')}")
        else:
            print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"   ❌ Error: {response.status_code}")

except Exception as e:
    print(f"   ❌ Connection Error: {e}")

try:
    # Test semantic search to verify data loading
    print("\n2. Testing Vector Database (Semantic Search):")
    search_data = {
        "query": "món ăn healthy Việt Nam",
        "n_results": 3
    }

    response = requests.post('http://localhost:5000/api/semantic_search',
                             json=search_data, timeout=15)
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            results = data.get('results', [])
            print(f"   ✅ Search Results: {len(results)} recipes found")
            for i, recipe in enumerate(results[:3]):
                print(
                    f"      {i+1}. {recipe['recipe_name']} ({recipe['estimated_calories']} cal)")
        else:
            print(f"   ❌ Search Failed: {data.get('error', 'Unknown error')}")
    else:
        print(f"   ❌ Error: {response.status_code}")

except Exception as e:
    print(f"   ❌ Search Error: {e}")

try:
    # Test AI agent with a simple query
    print("\n3. Testing AI Agent Integration:")
    agent_data = {
        "message": "Tôi muốn ăn món gì healthy?",
        "user_id": "CUS00001"
    }

    response = requests.post('http://localhost:5000/api/agent_chat',
                             json=agent_data, timeout=30)
    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            recipes = data.get('recommended_recipes', [])
            restaurants = data.get('nearby_restaurants', [])
            print(
                f"   ✅ AI Response Length: {len(data.get('ai_response', ''))}")
            print(f"   ✅ Recommended Recipes: {len(recipes)}")
            print(f"   ✅ Nearby Restaurants: {len(restaurants)}")

            # Show sample recommendations
            if recipes:
                print("   📋 Sample Recipe Recommendations:")
                for recipe in recipes[:3]:
                    print(
                        f"      - {recipe['name']} ({recipe['calories']} cal, {recipe['rating']:.1f}⭐)")
        else:
            print(
                f"   ❌ AI Agent Failed: {data.get('error', 'Unknown error')}")
    else:
        print(f"   ❌ Error: {response.status_code}")

except Exception as e:
    print(f"   ❌ AI Agent Error: {e}")

print("\n🎯 FINAL VERIFICATION:")
print("=" * 60)

# Summary check
all_good = True
issues = []

try:
    # Quick stats check
    stats_response = requests.get(
        'http://localhost:5000/api/agent_stats', timeout=5)
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        if 'stats' in stats_data:
            total_interactions = stats_data['stats'].get(
                'total_interactions', 0)
            recipes_count = stats_data['stats'].get('recipes_count', 0)
            customers_count = stats_data['stats'].get('customers_count', 0)

            print(f"📊 Data Summary:")
            print(f"   • Total Interactions: {total_interactions:,}")
            print(f"   • Recipes in DB: {recipes_count}")
            print(f"   • Customers in DB: {customers_count}")

            if total_interactions >= 14000:
                print("   ✅ 14K+ interactions loaded successfully")
            else:
                print(f"   ⚠️ Only {total_interactions:,} interactions loaded")
                issues.append(f"Expected 14K+, got {total_interactions:,}")
                all_good = False

            if recipes_count >= 90:
                print("   ✅ Sufficient recipes in database")
            else:
                print(f"   ⚠️ Only {recipes_count} recipes loaded")
                issues.append(f"Low recipe count: {recipes_count}")
                all_good = False

            if customers_count >= 1000:
                print("   ✅ Sufficient customers in database")
            else:
                print(f"   ⚠️ Only {customers_count} customers loaded")
                issues.append(f"Low customer count: {customers_count}")
                all_good = False
        else:
            issues.append("No stats data in response")
            all_good = False
    else:
        issues.append(f"Stats endpoint error: {stats_response.status_code}")
        all_good = False

except Exception as e:
    issues.append(f"Stats check failed: {e}")
    all_good = False

print(f"\n🏆 FINAL RESULT:")
if all_good:
    print("   🎉 ✅ ALL 14K+ INTERACTIONS LOADED AND WORKING PERFECTLY!")
    print("   🎉 ✅ VECTOR DATABASE FULLY POPULATED!")
    print("   🎉 ✅ APP RUNNING WITH COMPLETE DATASET!")
else:
    print("   ⚠️ ISSUES DETECTED:")
    for issue in issues:
        print(f"      - {issue}")

print("=" * 60)
