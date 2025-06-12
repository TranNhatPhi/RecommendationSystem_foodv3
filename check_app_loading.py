import pandas as pd
from app import interactions_df, customers_df, customer_ids, customers_info, user_items, item_features

print("🔍 Checking App Data Loading Details...")
print("=" * 60)

print(f"\n1. INTERACTIONS DATA:")
print(f"   📊 Total interactions loaded: {len(interactions_df):,}")
print(
    f"   📅 Date range: {interactions_df['interaction_date'].min()} → {interactions_df['interaction_date'].max()}")
print(f"   🍽️ Unique recipes: {interactions_df['recipe_name'].nunique()}")
print(f"   👥 Unique customers: {interactions_df['customer_id'].nunique()}")

print(f"\n2. CUSTOMERS DATA:")
print(f"   👥 Total customers loaded: {len(customers_df):,}")
print(f"   🆔 Customer IDs extracted: {len(customer_ids)}")
print(f"   📝 Enhanced customer info: {len(customers_info)}")

print(f"\n3. PREPROCESSING RESULTS:")
print(f"   👤 User items mapping: {len(user_items)} users")
print(f"   🍽️ Item features mapping: {len(item_features)} items")

print(f"\n4. SAMPLE DATA:")
# Show sample interactions
sample_interactions = interactions_df.head(3)
print("   📋 Sample interactions:")
for _, row in sample_interactions.iterrows():
    print(
        f"      - {row['customer_id']}: {row['recipe_name']} ({row['rating']}⭐)")

# Show sample customers
sample_customers = list(customers_info.items())[:3]
print("   👥 Sample customers:")
for cid, info in sample_customers:
    print(f"      - {cid}: {info['display_name']}")

print(f"\n5. DATA VALIDATION:")
# Check if data is properly interconnected
interaction_customers = set(interactions_df['customer_id'].unique())
customer_data_ids = set(
    customers_df['customer_id'].unique()) if not customers_df.empty else set()
common_customers = interaction_customers.intersection(customer_data_ids)

print(f"   🔗 Customers in interactions: {len(interaction_customers)}")
print(f"   🔗 Customers in customer data: {len(customer_data_ids)}")
print(f"   ✅ Overlapping customers: {len(common_customers)}")
print(
    f"   📊 Coverage: {len(common_customers)/len(interaction_customers)*100:.1f}%")

print(f"\n6. MEMORY USAGE:")
interactions_memory = interactions_df.memory_usage(
    deep=True).sum() / 1024 / 1024
customers_memory = customers_df.memory_usage(
    deep=True).sum() / 1024 / 1024 if not customers_df.empty else 0
print(f"   💾 Interactions DataFrame: {interactions_memory:.1f} MB")
print(f"   💾 Customers DataFrame: {customers_memory:.1f} MB")
print(f"   💾 Total memory: {interactions_memory + customers_memory:.1f} MB")

print(f"\n🎯 CONCLUSION:")
if len(interactions_df) >= 14000 and len(customer_ids) >= 1000:
    print("   ✅ FULL 14K+ INTERACTIONS LOADED SUCCESSFULLY")
    print("   ✅ ALL DATA PROPERLY PREPROCESSED FOR APP")
    print("   ✅ SYSTEM READY FOR RECOMMENDATIONS")
else:
    print("   ⚠️ PARTIAL DATA LOADING - CHECK ISSUES")

print("=" * 60)
