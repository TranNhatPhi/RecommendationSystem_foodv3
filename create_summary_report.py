import pandas as pd


def create_data_summary():
    print("📋 TẠO BÁO CÁO TỔNG KẾT DỮ LIỆU")
    print("=" * 40)

    try:
        df = pd.read_csv('interactions_enhanced_final.csv')
        print(f"✅ Đọc file thành công: {len(df):,} dòng")
    except:
        print("❌ Không thể đọc file interactions_enhanced_final.csv")
        return

    # 1. Summary statistics
    summary_stats = {
        'Metric': [
            'Tổng số interactions',
            'Số khách hàng unique',
            'Số món ăn unique',
            'Số loại interaction',
            'Rating trung bình',
            'Calories trung bình',
            'Thời gian chuẩn bị TB (phút)',
            'Giá tiền trung bình (VND)',
            'Số nguyên liệu trung bình'
        ],
        'Value': [
            f"{len(df):,}",
            f"{df['customer_id'].nunique():,}",
            f"{df['recipe_name'].nunique():,}",
            f"{df['interaction_type'].nunique()}",
            f"{df['rating'].mean():.2f}",
            f"{df['estimated_calories'].mean():.0f}" if 'estimated_calories' in df.columns else "N/A",
            f"{df['preparation_time_minutes'].mean():.0f}" if 'preparation_time_minutes' in df.columns else "N/A",
            f"{df['estimated_price_vnd'].mean():.0f}" if 'estimated_price_vnd' in df.columns else "N/A",
            f"{df['ingredient_count'].mean():.1f}" if 'ingredient_count' in df.columns else "N/A"
        ]
    }

    summary_df = pd.DataFrame(summary_stats)

    # 2. Nutrition category distribution
    if 'nutrition_category' in df.columns:
        nutrition_dist = df['nutrition_category'].value_counts().reset_index()
        nutrition_dist.columns = ['Nutrition Category', 'Count']
        nutrition_dist['Percentage'] = (
            nutrition_dist['Count'] / len(df) * 100).round(1)

    # 3. Meal time distribution
    meal_dist = df['meal_time'].value_counts().reset_index()
    meal_dist.columns = ['Meal Time', 'Count']
    meal_dist['Percentage'] = (meal_dist['Count'] / len(df) * 100).round(1)

    # 4. Difficulty distribution
    difficulty_dist = df['difficulty'].value_counts().reset_index()
    difficulty_dist.columns = ['Difficulty', 'Count']
    difficulty_dist['Percentage'] = (
        difficulty_dist['Count'] / len(df) * 100).round(1)

    # 5. Top recipes by interaction count
    top_recipes = df['recipe_name'].value_counts().head(10).reset_index()
    top_recipes.columns = ['Recipe Name', 'Interaction Count']

    # 6. Customer interaction summary
    customer_stats = df.groupby('customer_id').agg({
        'recipe_name': 'count',
        'rating': 'mean'
    }).reset_index()
    customer_stats.columns = ['Customer ID',
                              'Total Interactions', 'Avg Rating']
    customer_stats = customer_stats.sort_values(
        'Total Interactions', ascending=False).head(10)

    # Save all summaries to Excel file
    with pd.ExcelWriter('data_summary_report.xlsx', engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='Overview', index=False)

        if 'nutrition_category' in df.columns:
            nutrition_dist.to_excel(
                writer, sheet_name='Nutrition Distribution', index=False)

        meal_dist.to_excel(
            writer, sheet_name='Meal Time Distribution', index=False)
        difficulty_dist.to_excel(
            writer, sheet_name='Difficulty Distribution', index=False)
        top_recipes.to_excel(writer, sheet_name='Top Recipes', index=False)
        customer_stats.to_excel(
            writer, sheet_name='Top Customers', index=False)

    # Print summary to console
    print("\n📊 TỔNG QUAN DỮ LIỆU:")
    print(summary_df.to_string(index=False))

    if 'nutrition_category' in df.columns:
        print(f"\n🥗 PHÂN BỐ NUTRITION CATEGORIES:")
        for _, row in nutrition_dist.iterrows():
            print(
                f"- {row['Nutrition Category']}: {row['Count']} ({row['Percentage']}%)")

    print(f"\n🍽️ PHÂN BỐ MEAL TIME:")
    for _, row in meal_dist.iterrows():
        print(f"- {row['Meal Time']}: {row['Count']} ({row['Percentage']}%)")

    print(f"\n📈 TOP 5 MÓN ĂN PHỔ BIẾN:")
    for _, row in top_recipes.head().iterrows():
        print(
            f"- {row['Recipe Name']}: {row['Interaction Count']} interactions")

    print(f"\n✅ Báo cáo chi tiết đã được lưu: data_summary_report.xlsx")


if __name__ == "__main__":
    create_data_summary()
