import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Load và phân tích dữ liệu hiện tại


def analyze_current_data():
    try:
        df = pd.read_csv('interactions_encoded.csv', encoding='utf-8')
        print("✅ Đọc file CSV thành công với UTF-8")
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('interactions_encoded.csv', encoding='latin-1')
            print("✅ Đọc file CSV thành công với Latin-1")
        except:
            df = pd.read_csv('interactions_encoded.csv', encoding='cp1252')
            print("✅ Đọc file CSV thành công với CP1252")

    print(f"\n📊 THỐNG KÊ DỮ LIỆU HIỆN TẠI:")
    print(f"- Tổng số dòng: {len(df):,}")
    print(f"- Tổng số cột: {len(df.columns)}")
    print(f"- Số khách hàng unique: {df['customer_id'].nunique()}")
    print(f"- Số món ăn unique: {df['recipe_name'].nunique()}")
    print(f"- Số interaction types: {df['interaction_type'].nunique()}")

    print(f"\n🏷️ CÁC CỘT HIỆN TẠI:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")

    print(f"\n📈 THỐNG KÊ CHI TIẾT:")
    print(
        f"- Rating range: {df['rating'].min():.1f} - {df['rating'].max():.1f}")
    print(f"- Interaction types: {list(df['interaction_type'].unique())}")
    print(f"- Difficulties: {list(df['difficulty'].unique())}")
    print(f"- Meal times: {list(df['meal_time'].unique())}")

    # Kiểm tra dữ liệu thiếu
    print(f"\n❗ DỮ LIỆU THIẾU:")
    missing_data = df.isnull().sum()
    for col in missing_data[missing_data > 0].index:
        print(
            f"- {col}: {missing_data[col]} dòng thiếu ({missing_data[col]/len(df)*100:.1f}%)")

    # Kiểm tra các giá trị 'unknown'
    print(f"\n🔍 GIÁ TRỊ 'UNKNOWN':")
    if 'meal_time' in df.columns:
        unknown_meal = (df['meal_time'] == 'unknown').sum()
        print(
            f"- Meal time 'unknown': {unknown_meal} ({unknown_meal/len(df)*100:.1f}%)")

    if 'difficulty' in df.columns:
        unknown_diff = (df['difficulty'] == 'Không rõ').sum()
        print(
            f"- Difficulty 'Không rõ': {unknown_diff} ({unknown_diff/len(df)*100:.1f}%)")

    return df

# Bổ sung các trường dữ liệu cần thiết cho nutrition recommendations


def enhance_data_for_nutrition(df):
    print(f"\n🔧 BỔ SUNG DỮ LIỆU CHO NUTRITION RECOMMENDATIONS...")

    # 1. Bổ sung nutrition_category
    nutrition_keywords = {
        'weight-loss': ['salad', 'gỏi', 'canh', 'luộc', 'hấp', 'nướng', 'rau', 'cá', 'soup'],
        'blood-boost': ['thịt', 'gan', 'rau dền', 'rau chân vịt', 'đậu', 'trứng', 'cà chua'],
        'brain-boost': ['cá', 'hạt', 'trứng', 'bơ', 'chocolate', 'óc chó'],
        'digestive-support': ['cháo', 'soup', 'canh', 'yogurt', 'gừng', 'nghệ', 'yến mạch'],
        'balanced': ['cơm', 'phở', 'bún', 'bánh', 'mì']
    }

    def categorize_nutrition(recipe_name):
        recipe_lower = recipe_name.lower()
        categories = []

        for category, keywords in nutrition_keywords.items():
            if any(keyword in recipe_lower for keyword in keywords):
                categories.append(category)

        if not categories:
            return 'balanced'
        return categories[0]  # Trả về category đầu tiên nếu có nhiều

    df['nutrition_category'] = df['recipe_name'].apply(categorize_nutrition)

    # 2. Bổ sung calories estimate
    def estimate_calories(recipe_name, meal_time, difficulty):
        base_calories = {
            'breakfast': 350,
            'lunch': 550,
            'dinner': 500,
            'unknown': 450
        }

        difficulty_multiplier = {
            'Dễ': 0.9,
            'Trung bình': 1.0,
            'Khó': 1.2,
            'Không rõ': 1.0
        }

        # Keyword adjustments
        recipe_lower = recipe_name.lower()
        if any(word in recipe_lower for word in ['salad', 'gỏi', 'canh']):
            calories_adj = 0.7
        elif any(word in recipe_lower for word in ['thịt', 'gà', 'heo', 'bò']):
            calories_adj = 1.3
        elif any(word in recipe_lower for word in ['cháo', 'soup']):
            calories_adj = 0.8
        else:
            calories_adj = 1.0

        base = base_calories.get(meal_time, 450)
        multiplier = difficulty_multiplier.get(difficulty, 1.0)

        estimated = int(base * multiplier * calories_adj)
        # Add some randomness
        estimated += random.randint(-50, 50)

        return max(100, estimated)  # Minimum 100 calories

    df['estimated_calories'] = df.apply(
        lambda row: estimate_calories(
            row['recipe_name'], row['meal_time'], row['difficulty']),
        axis=1
    )

    # 3. Bổ sung preparation_time
    def estimate_prep_time(difficulty):
        time_ranges = {
            'Dễ': (15, 30),
            'Trung bình': (30, 60),
            'Khó': (60, 120),
            'Không rõ': (20, 45)
        }
        min_time, max_time = time_ranges.get(difficulty, (20, 45))
        return random.randint(min_time, max_time)

    df['preparation_time_minutes'] = df['difficulty'].apply(estimate_prep_time)

    # 4. Bổ sung ingredient_count
    def estimate_ingredients(difficulty, recipe_name):
        base_counts = {
            'Dễ': (3, 6),
            'Trung bình': (5, 10),
            'Khó': (8, 15),
            'Không rõ': (4, 8)
        }

        min_count, max_count = base_counts.get(difficulty, (4, 8))

        # Adjust based on recipe name complexity
        if len(recipe_name) > 30:
            max_count += 2

        return random.randint(min_count, max_count)

    df['ingredient_count'] = df.apply(
        lambda row: estimate_ingredients(
            row['difficulty'], row['recipe_name']),
        axis=1
    )

    # 5. Bổ sung price_range
    def estimate_price_range(difficulty, ingredient_count):
        base_prices = {
            'Dễ': (20000, 50000),
            'Trung bình': (40000, 80000),
            'Khó': (60000, 120000),
            'Không rõ': (30000, 60000)
        }

        min_price, max_price = base_prices.get(difficulty, (30000, 60000))

        # Adjust based on ingredient count
        price_per_ingredient = random.randint(3000, 8000)
        estimated_price = min_price + (ingredient_count * price_per_ingredient)

        return min(estimated_price, max_price)

    df['estimated_price_vnd'] = df.apply(
        lambda row: estimate_price_range(
            row['difficulty'], row['ingredient_count']),
        axis=1
    )

    # 6. Cải thiện meal_time cho các 'unknown'
    def improve_meal_time(recipe_name, current_meal_time):
        if current_meal_time != 'unknown':
            return current_meal_time

        recipe_lower = recipe_name.lower()

        # Breakfast keywords
        if any(word in recipe_lower for word in ['bánh', 'sữa', 'trứng', 'cháo', 'phở']):
            return 'breakfast'
        # Lunch keywords
        elif any(word in recipe_lower for word in ['cơm', 'bún', 'mì', 'canh', 'salad']):
            return 'lunch'
        # Dinner keywords
        elif any(word in recipe_lower for word in ['thịt', 'gà', 'cá', 'tôm', 'nướng', 'rim']):
            return 'dinner'
        else:
            return random.choice(['breakfast', 'lunch', 'dinner'])

    df['meal_time'] = df.apply(
        lambda row: improve_meal_time(row['recipe_name'], row['meal_time']),
        axis=1
    )

    # Update meal_time_code accordingly
    meal_time_mapping = {'breakfast': 0, 'lunch': 2, 'dinner': 1}
    df['meal_time_code'] = df['meal_time'].map(meal_time_mapping).fillna(3)

    # 7. Cải thiện difficulty cho 'Không rõ'
    def improve_difficulty(recipe_name, current_difficulty):
        if current_difficulty != 'Không rõ':
            return current_difficulty

        recipe_lower = recipe_name.lower()

        # Easy indicators
        if any(word in recipe_lower for word in ['salad', 'gỏi', 'luộc', 'hấp']):
            return 'Dễ'
        # Hard indicators
        elif any(word in recipe_lower for word in ['nướng', 'rim', 'om', 'braised']):
            return 'Trung bình'
        else:
            return random.choice(['Dễ', 'Trung bình'])

    df['difficulty'] = df.apply(
        lambda row: improve_difficulty(row['recipe_name'], row['difficulty']),
        axis=1
    )

    # Update difficulty_code
    difficulty_mapping = {'Dễ': 0, 'Trung bình': 3, 'Khó': 1}
    df['difficulty_code'] = df['difficulty'].map(difficulty_mapping).fillna(2)

    return df

# Tạo thêm dữ liệu đa dạng


def add_more_diverse_data(df):
    print(f"\n➕ THÊM DỮ LIỆU ĐA DẠNG...")

    # Tạo thêm khách hàng mới
    max_customer_num = max([int(cid.replace('CUS', ''))
                           for cid in df['customer_id'].unique()])
    new_customers = [f"CUS{i:05d}" for i in range(
        max_customer_num + 1, max_customer_num + 51)]

    # Tạo thêm món ăn mới
    additional_recipes = [
        ("Salad rau củ quả", "https://monngonmoingay.com/salad-rau-cu-qua/", "weight-loss"),
        ("Cháo yến mạch hạt chia",
         "https://monngonmoingay.com/chao-yen-mach/", "digestive-support"),
        ("Cá hồi nướng bơ tỏi", "https://monngonmoingay.com/ca-hoi-nuong/", "brain-boost"),
        ("Canh rau dền nấu tôm", "https://monngonmoingay.com/canh-rau-den/", "blood-boost"),
        ("Thịt bò xào súp lơ", "https://monngonmoingay.com/thit-bo-xao-sup-lo/", "balanced"),
        ("Smoothie xanh detox", "https://monngonmoingay.com/smoothie-xanh/", "weight-loss"),
        ("Gà nướng mật ong", "https://monngonmoingay.com/ga-nuong-mat-ong/", "balanced"),
        ("Canh chua cá bông lau",
         "https://monngonmoingay.com/canh-chua-ca/", "digestive-support"),
        ("Bánh mì sandwich healthy",
         "https://monngonmoingay.com/banh-mi-healthy/", "weight-loss"),
        ("Tôm rang me", "https://monngonmoingay.com/tom-rang-me/", "balanced")
    ]

    new_rows = []
    interaction_types = ['like', 'view', 'save', 'cook', 'rate']
    comments = [
        "Món ăn tuyệt vời!",
        "Rất ngon và bổ dưỡng",
        "Hương vị hài hòa, rất đáng thử",
        "Món ăn ổn, có thể cải thiện thêm một chút",
        "Thưởng thức tuyệt vời, món ăn thật sự xuất sắc!",
        "Không thực sự ấn tượng, cần tinh chỉnh lại hương vị",
        "Khó thưởng thức, món chưa đạt yêu cầu"
    ]

    for customer in new_customers[:30]:  # Chỉ thêm 30 khách hàng mới
        user_index = df['user_index'].max() + 1

        # Mỗi khách hàng có 3-8 interactions
        num_interactions = random.randint(3, 8)

        for _ in range(num_interactions):
            # Chọn ngẫu nhiên từ món ăn hiện có hoặc món mới
            if random.random() < 0.3:  # 30% chance món mới
                recipe_info = random.choice(additional_recipes)
                recipe_name, recipe_url, nutrition_cat = recipe_info
                item_index = df['item_index'].max() + random.randint(1, 10)
            else:  # 70% chance món hiện có
                existing_recipe = df.sample(1).iloc[0]
                recipe_name = existing_recipe['recipe_name']
                recipe_url = existing_recipe['recipe_url']
                nutrition_cat = existing_recipe.get(
                    'nutrition_category', 'balanced')
                item_index = existing_recipe['item_index']

            interaction_type = random.choice(interaction_types)
            rating = round(random.uniform(1.5, 5.0), 1)

            # Generate random date within last year
            start_date = datetime.now() - timedelta(days=365)
            random_date = start_date + timedelta(days=random.randint(0, 365))

            comment = random.choice(comments)

            # Generate other fields
            difficulty = random.choice(['Dễ', 'Trung bình', 'Khó'])
            meal_time = random.choice(['breakfast', 'lunch', 'dinner'])

            new_row = {
                'customer_id': customer,
                'recipe_name': recipe_name,
                'recipe_url': recipe_url,
                'interaction_type': interaction_type,
                'rating': rating,
                'interaction_date': random_date.strftime('%Y-%m-%d'),
                'comment': comment,
                'user_index': user_index,
                'item_index': item_index,
                'content_score': round(random.uniform(0.1, 0.4), 10),
                'cf_score': round(random.uniform(2.5, 3.5), 10),
                'interaction_type_code': interaction_types.index(interaction_type),
                'difficulty': difficulty,
                'difficulty_code': ['Dễ', 'Khó', 'Không rõ', 'Trung bình'].index(difficulty),
                'meal_time': meal_time,
                'meal_time_code': ['breakfast', 'dinner', 'lunch'].index(meal_time),
                'nutrition_category': nutrition_cat,
                'estimated_calories': random.randint(200, 800),
                'preparation_time_minutes': random.randint(15, 90),
                'ingredient_count': random.randint(3, 12),
                'estimated_price_vnd': random.randint(20000, 100000)
            }

            new_rows.append(new_row)

    # Thêm các dòng mới vào DataFrame
    new_df = pd.DataFrame(new_rows)
    enhanced_df = pd.concat([df, new_df], ignore_index=True)

    print(f"✅ Đã thêm {len(new_rows)} dòng dữ liệu mới")

    return enhanced_df


def main():
    print("🔍 PHÂN TÍCH VÀ BỔ SUNG DỮ LIỆU CSV")
    print("=" * 50)

    # Phân tích dữ liệu hiện tại
    df = analyze_current_data()

    # Bổ sung dữ liệu cho nutrition recommendations
    enhanced_df = enhance_data_for_nutrition(df)

    # Thêm dữ liệu đa dạng
    final_df = add_more_diverse_data(enhanced_df)

    # Lưu file mới
    output_file = 'interactions_enhanced_final.csv'
    final_df.to_csv(output_file, index=False, encoding='utf-8')

    print(f"\n✅ HOÀN THÀNH!")
    print(f"📄 File đã được lưu: {output_file}")
    print(f"📊 Tổng số dòng: {len(final_df):,}")
    print(f"👥 Tổng số khách hàng: {final_df['customer_id'].nunique()}")
    print(f"🍽️ Tổng số món ăn: {final_df['recipe_name'].nunique()}")

    print(f"\n🆕 CÁC CỘT MỚI ĐÃ THÊM:")
    new_columns = ['nutrition_category', 'estimated_calories', 'preparation_time_minutes',
                   'ingredient_count', 'estimated_price_vnd']
    for i, col in enumerate(new_columns, 1):
        print(f"{i}. {col}")

    print(f"\n📈 PHÂN BỐ NUTRITION CATEGORIES:")
    nutrition_dist = final_df['nutrition_category'].value_counts()
    for category, count in nutrition_dist.items():
        print(f"- {category}: {count} ({count/len(final_df)*100:.1f}%)")


if __name__ == "__main__":
    main()
