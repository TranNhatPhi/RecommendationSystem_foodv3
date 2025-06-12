import pandas as pd
import os
import json
from typing import List, Dict, Optional
import sqlite3
from datetime import datetime


class SimpleFoodRecommendationDB:
    def __init__(self, db_path="./simple_food_db.sqlite"):
        """Initialize simple SQLite database for food recommendations"""
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT NOT NULL,
                recipe_url TEXT,
                difficulty TEXT,
                meal_time TEXT,
                nutrition_category TEXT,
                estimated_calories REAL,
                preparation_time_minutes REAL,
                ingredient_count INTEGER,
                estimated_price_vnd REAL,
                avg_rating REAL,
                content_score REAL,
                cf_score REAL,
                keywords TEXT
            )
        ''')

        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL UNIQUE,
                full_name TEXT,
                gender TEXT,
                age_group TEXT,
                region TEXT,
                registration_date TEXT
            )
        ''')

        # Create search index table for simple text search
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                keyword TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')

        # Create interactions table to store ALL 14k interactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                recipe_name TEXT NOT NULL,
                recipe_url TEXT,
                difficulty TEXT,
                meal_time TEXT,
                nutrition_category TEXT,
                estimated_calories REAL,
                preparation_time_minutes REAL,
                ingredient_count INTEGER,
                estimated_price_vnd REAL,
                rating REAL,
                interaction_type TEXT,
                interaction_date TEXT,
                content_score REAL,
                cf_score REAL,
                item_index INTEGER,
                comment TEXT
            )
        ''')

        # Create index for faster queries
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_customer_id ON interactions(customer_id)')
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_recipe_name ON interactions(recipe_name)')
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_interaction_date ON interactions(interaction_date)')

        conn.commit()
        conn.close()

    def populate_recipes(self, interactions_file="interactions_enhanced_final.csv"):
        """Populate recipes from CSV file"""
        try:
            df = pd.read_csv(interactions_file)
            print(f"Loading {len(df)} interactions from {interactions_file}")

            # Group by recipe to avoid duplicates
            recipe_groups = df.groupby('recipe_name').agg({
                'recipe_url': 'first',
                'difficulty': 'first',
                'meal_time': 'first',
                'nutrition_category': 'first',
                'estimated_calories': 'first',
                'preparation_time_minutes': 'first',
                'ingredient_count': 'first',
                'estimated_price_vnd': 'first',
                'rating': 'mean',
                'content_score': 'mean',
                'cf_score': 'mean',
                'comment': lambda x: ' '.join(x.dropna().astype(str))
            }).reset_index()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clear existing data
            cursor.execute('DELETE FROM recipes')
            cursor.execute('DELETE FROM search_keywords')

            for idx, row in recipe_groups.iterrows():
                # Create keywords for search
                keywords = self._create_keywords(row)

                # Insert recipe
                cursor.execute('''
                    INSERT INTO recipes (
                        recipe_name, recipe_url, difficulty, meal_time, nutrition_category,
                        estimated_calories, preparation_time_minutes, ingredient_count,
                        estimated_price_vnd, avg_rating, content_score, cf_score, keywords
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(row['recipe_name']),
                    str(row['recipe_url']),
                    str(row['difficulty']),
                    str(row['meal_time']),
                    str(row['nutrition_category']),
                    float(row['estimated_calories']) if pd.notna(
                        row['estimated_calories']) else 0,
                    float(row['preparation_time_minutes']) if pd.notna(
                        row['preparation_time_minutes']) else 0,
                    int(row['ingredient_count']) if pd.notna(
                        row['ingredient_count']) else 0,
                    float(row['estimated_price_vnd']) if pd.notna(
                        row['estimated_price_vnd']) else 0,
                    float(row['rating']) if pd.notna(row['rating']) else 0,
                    float(row['content_score']) if pd.notna(
                        row['content_score']) else 0,
                    float(row['cf_score']) if pd.notna(row['cf_score']) else 0,
                    keywords
                ))

                recipe_id = cursor.lastrowid

                # Insert search keywords
                for keyword in keywords.split():
                    if len(keyword) > 2:  # Only keywords longer than 2 chars
                        cursor.execute('INSERT INTO search_keywords (recipe_id, keyword) VALUES (?, ?)',
                                       (recipe_id, keyword.lower()))

            conn.commit()
            conn.close()

            print(
                f"✅ Successfully added {len(recipe_groups)} recipes to database")
            return True

        except Exception as e:
            print(f"❌ Error populating recipes: {str(e)}")
            return False

    def populate_customers(self, customers_file="customers_data.csv"):
        """Populate customers from CSV file"""
        try:
            df = pd.read_csv(customers_file)
            print(f"Loading {len(df)} customers from {customers_file}")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clear existing data
            cursor.execute('DELETE FROM customers')

            for idx, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO customers (
                        customer_id, full_name, gender, age_group, region, registration_date
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    str(row['customer_id']),
                    str(row['full_name']),
                    str(row['gender']),
                    str(row['age_group']),
                    str(row['region']),
                    str(row['registration_date'])
                ))

            conn.commit()
            conn.close()

            print(f"✅ Successfully added {len(df)} customers to database")
            return True

        except Exception as e:
            print(f"❌ Error populating customers: {str(e)}")
            return False

    def populate_all_interactions(self, interactions_file="interactions_enhanced_final.csv"):
        """Populate ALL 14k+ interactions from CSV file (not just unique recipes)"""
        try:
            df = pd.read_csv(interactions_file)
            print(
                f"🔥 Loading ALL {len(df)} interactions from {interactions_file}")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clear existing interactions data
            cursor.execute('DELETE FROM interactions')

            # Insert ALL interactions (not grouped)
            for idx, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO interactions (
                        customer_id, recipe_name, recipe_url, difficulty, meal_time,
                        nutrition_category, estimated_calories, preparation_time_minutes,
                        ingredient_count, estimated_price_vnd, rating, interaction_type,
                        interaction_date, content_score, cf_score, item_index, comment
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(row['customer_id']),
                    str(row['recipe_name']),
                    str(row.get('recipe_url', '')),
                    str(row.get('difficulty', '')),
                    str(row.get('meal_time', '')),
                    str(row.get('nutrition_category', '')),
                    float(row['estimated_calories']) if pd.notna(
                        row.get('estimated_calories')) else 0,
                    float(row['preparation_time_minutes']) if pd.notna(
                        row.get('preparation_time_minutes')) else 0,
                    int(row['ingredient_count']) if pd.notna(
                        row.get('ingredient_count')) else 0,
                    float(row['estimated_price_vnd']) if pd.notna(
                        row.get('estimated_price_vnd')) else 0,
                    float(row['rating']) if pd.notna(row.get('rating')) else 0,
                    str(row.get('interaction_type', '')),
                    str(row.get('interaction_date', '')),
                    float(row['content_score']) if pd.notna(
                        row.get('content_score')) else 0,
                    float(row['cf_score']) if pd.notna(
                        row.get('cf_score')) else 0,
                    int(row['item_index']) if pd.notna(
                        row.get('item_index')) else 0,
                    str(row.get('comment', ''))
                ))

                # Print progress every 1000 rows
                if (idx + 1) % 1000 == 0:
                    print(f"   Loaded {idx + 1}/{len(df)} interactions...")

            conn.commit()
            conn.close()

            print(
                f"🎉 ✅ Successfully loaded ALL {len(df)} interactions to database!")
            return True

        except Exception as e:
            print(f"❌ Error loading all interactions: {str(e)}")
            return False

    def _create_keywords(self, row):
        """Create searchable keywords from recipe data"""
        keywords = []

        # Add recipe name words
        keywords.extend(str(row['recipe_name']).lower().split())

        # Add category and meal time
        keywords.append(str(row['nutrition_category']).lower())
        keywords.append(str(row['meal_time']).lower())
        keywords.append(str(row['difficulty']).lower())

        # Add comment words (first 10 words)
        if pd.notna(row['comment']):
            comment_words = str(row['comment']).lower().split()[:10]
            keywords.extend(comment_words)

        return ' '.join(keywords)

    def search_recipes(self, query: str, filters: Dict = None, n_results: int = 5):
        """Search recipes using simple text matching"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Build base query
            base_query = '''
                SELECT DISTINCT r.* FROM recipes r
                LEFT JOIN search_keywords sk ON r.id = sk.recipe_id
                WHERE 1=1
            '''
            params = []

            # Add text search
            if query:
                query_words = query.lower().split()
                search_conditions = []
                for word in query_words:
                    if len(word) > 2:
                        search_conditions.append(
                            '(r.keywords LIKE ? OR sk.keyword LIKE ?)')
                        params.extend([f'%{word}%', f'%{word}%'])

                if search_conditions:
                    base_query += ' AND (' + \
                        ' OR '.join(search_conditions) + ')'

            # Add filters
            if filters:
                if 'difficulty' in filters:
                    base_query += ' AND r.difficulty = ?'
                    params.append(filters['difficulty'])

                if 'meal_time' in filters:
                    base_query += ' AND r.meal_time = ?'
                    params.append(filters['meal_time'])

                if 'nutrition_category' in filters:
                    base_query += ' AND r.nutrition_category = ?'
                    params.append(filters['nutrition_category'])

                if 'max_calories' in filters:
                    base_query += ' AND r.estimated_calories <= ?'
                    params.append(filters['max_calories'])

                if 'max_time' in filters:
                    base_query += ' AND r.preparation_time_minutes <= ?'
                    params.append(filters['max_time'])

            # Order by rating and content score
            base_query += ' ORDER BY r.avg_rating DESC, r.content_score DESC LIMIT ?'
            params.append(n_results)

            cursor.execute(base_query, params)
            results = cursor.fetchall()
            conn.close()

            # Format results
            if results:
                columns = ['id', 'recipe_name', 'recipe_url', 'difficulty', 'meal_time',
                           'nutrition_category', 'estimated_calories', 'preparation_time_minutes',
                           'ingredient_count', 'estimated_price_vnd', 'avg_rating', 'content_score',
                           'cf_score', 'keywords']

                formatted_results = {
                    'documents': [[]],
                    'metadatas': [[]],
                    'distances': [[]]
                }

                for result in results:
                    result_dict = dict(zip(columns, result))

                    # Create document text
                    doc_text = f"Tên món: {result_dict['recipe_name']}\nLoại: {result_dict['nutrition_category']}\nĐộ khó: {result_dict['difficulty']}"
                    formatted_results['documents'][0].append(doc_text)

                    # Create metadata
                    meta = {
                        'recipe_name': result_dict['recipe_name'],
                        'recipe_url': result_dict['recipe_url'],
                        'difficulty': result_dict['difficulty'],
                        'meal_time': result_dict['meal_time'],
                        'nutrition_category': result_dict['nutrition_category'],
                        'estimated_calories': result_dict['estimated_calories'],
                        'preparation_time_minutes': result_dict['preparation_time_minutes'],
                        'ingredient_count': result_dict['ingredient_count'],
                        'estimated_price_vnd': result_dict['estimated_price_vnd'],
                        'avg_rating': result_dict['avg_rating'],
                        'content_score': result_dict['content_score'],
                        'cf_score': result_dict['cf_score']
                    }
                    formatted_results['metadatas'][0].append(meta)
                    formatted_results['distances'][0].append(
                        0.5)  # Mock distance

                return formatted_results
            else:
                return None

        except Exception as e:
            print(f"❌ Error searching recipes: {str(e)}")
            return None

    def search_customers(self, query: str, filters: Dict = None, n_results: int = 5):
        """Search customers using simple text matching"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            base_query = 'SELECT * FROM customers WHERE 1=1'
            params = []

            if query:
                base_query += ' AND (customer_id LIKE ? OR full_name LIKE ? OR region LIKE ?)'
                params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])

            if filters:
                for key, value in filters.items():
                    base_query += f' AND {key} = ?'
                    params.append(value)

            base_query += f' LIMIT {n_results}'

            cursor.execute(base_query, params)
            results = cursor.fetchall()
            conn.close()

            if results:
                columns = ['id', 'customer_id', 'full_name', 'gender',
                           'age_group', 'region', 'registration_date']
                formatted_results = {
                    'documents': [[]],
                    'metadatas': [[]]
                }

                for result in results:
                    result_dict = dict(zip(columns, result))
                    doc_text = f"Khách hàng: {result_dict['full_name']}\nID: {result_dict['customer_id']}"
                    formatted_results['documents'][0].append(doc_text)
                    formatted_results['metadatas'][0].append(result_dict)

                return formatted_results
            else:
                return None

        except Exception as e:
            print(f"❌ Error searching customers: {str(e)}")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

    def search_all_interactions(self, query: str = "", filters: Dict = {}, n_results: int = 10):
        """Search ALL interactions (not just unique recipes)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            base_query = '''
                SELECT * FROM interactions
                WHERE 1=1
            '''
            params = []

            # Add text search across multiple fields
            if query:
                query_words = query.lower().split()
                search_conditions = []
                for word in query_words:
                    if len(word) > 2:
                        search_conditions.append('''
                            (LOWER(recipe_name) LIKE ? OR 
                             LOWER(nutrition_category) LIKE ? OR 
                             LOWER(difficulty) LIKE ? OR 
                             LOWER(meal_time) LIKE ? OR
                             LOWER(comment) LIKE ?)
                        ''')
                        params.extend([f'%{word}%'] * 5)

                if search_conditions:
                    base_query += ' AND (' + \
                        ' OR '.join(search_conditions) + ')'

            # Add filters
            if filters:
                if 'customer_id' in filters:
                    base_query += ' AND customer_id = ?'
                    params.append(filters['customer_id'])

                if 'difficulty' in filters:
                    base_query += ' AND difficulty = ?'
                    params.append(filters['difficulty'])

                if 'meal_time' in filters:
                    base_query += ' AND meal_time = ?'
                    params.append(filters['meal_time'])

                if 'nutrition_category' in filters:
                    base_query += ' AND nutrition_category = ?'
                    params.append(filters['nutrition_category'])

                if 'min_rating' in filters:
                    base_query += ' AND rating >= ?'
                    params.append(filters['min_rating'])

                if 'max_calories' in filters:
                    base_query += ' AND estimated_calories <= ?'
                    params.append(filters['max_calories'])

                if 'interaction_type' in filters:
                    base_query += ' AND interaction_type = ?'
                    params.append(filters['interaction_type'])

            # Order by rating and date
            base_query += ' ORDER BY rating DESC, interaction_date DESC LIMIT ?'
            params.append(n_results)

            cursor.execute(base_query, params)
            results = cursor.fetchall()
            conn.close()

            # Format results
            if results:
                columns = ['id', 'customer_id', 'recipe_name', 'recipe_url', 'difficulty',
                           'meal_time', 'nutrition_category', 'estimated_calories',
                           'preparation_time_minutes', 'ingredient_count', 'estimated_price_vnd',
                           'rating', 'interaction_type', 'interaction_date', 'content_score',
                           'cf_score', 'item_index', 'comment']

                formatted_results = {
                    'documents': [[]],
                    'metadatas': [[]],
                    'distances': [[]]
                }

                for result in results:
                    result_dict = dict(zip(columns, result))

                    # Create document text
                    doc_text = f"Customer: {result_dict['customer_id']}, Recipe: {result_dict['recipe_name']}, Rating: {result_dict['rating']}, Date: {result_dict['interaction_date']}"

                    formatted_results['documents'][0].append(doc_text)
                    formatted_results['metadatas'][0].append(result_dict)
                    formatted_results['distances'][0].append(
                        1.0)  # Default distance

                return formatted_results
            else:
                return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

        except Exception as e:
            print(f"❌ Error searching all interactions: {str(e)}")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

    def get_customer_interactions(self, customer_id: str, limit: int = 50):
        """Get all interactions for a specific customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM interactions 
                WHERE customer_id = ? 
                ORDER BY interaction_date DESC 
                LIMIT ?
            ''', (customer_id, limit))

            results = cursor.fetchall()
            conn.close()

            if results:
                columns = ['id', 'customer_id', 'recipe_name', 'recipe_url', 'difficulty',
                           'meal_time', 'nutrition_category', 'estimated_calories',
                           'preparation_time_minutes', 'ingredient_count', 'estimated_price_vnd',
                           'rating', 'interaction_type', 'interaction_date', 'content_score',
                           'cf_score', 'item_index', 'comment']

                return [dict(zip(columns, result)) for result in results]
            else:
                return []

        except Exception as e:
            print(f"❌ Error getting customer interactions: {str(e)}")
            return []


def main():
    """Main function to populate the simple database with ALL interactions"""
    print("🚀 Initializing Simple Food Recommendation Database...")

    # Initialize database
    db = SimpleFoodRecommendationDB()

    # Populate collections
    print("\n📚 Populating recipes collection...")
    db.populate_recipes()

    print("\n👥 Populating customers collection...")
    db.populate_customers()

    print("\n🔥 Populating ALL interactions...")
    db.populate_all_interactions()

    # Show statistics
    print("\n📊 Database Statistics:")
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM recipes')
    recipes_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM customers')
    customers_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM interactions')
    interactions_count = cursor.fetchone()[0]

    print(f"Recipes: {recipes_count}")
    print(f"Customers: {customers_count}")
    print(f"Interactions: {interactions_count}")
    conn.close()

    # Test search functionality
    print("\n🔍 Testing search functionality...")
    test_results = db.search_recipes(
        "món ăn Việt Nam truyền thống tốt cho sức khỏe", n_results=3)
    if test_results and test_results['documents']:
        print("Sample recipe search results:")
        for i, (doc, meta) in enumerate(zip(test_results['documents'][0], test_results['metadatas'][0])):
            print(
                f"{i+1}. {meta['recipe_name']} - {meta['nutrition_category']}")

    # Test new interaction search
    print("\n🔍 Testing interaction search functionality...")
    interaction_results = db.search_all_interactions("món Việt", n_results=3)
    if interaction_results and interaction_results['documents'][0]:
        print("Sample interaction search results:")
        for i, (doc, meta) in enumerate(zip(interaction_results['documents'][0], interaction_results['metadatas'][0])):
            print(
                f"{i+1}. Customer {meta['customer_id']}: {meta['recipe_name']} (Rating: {meta['rating']})")

    print("\n✅ Simple database setup complete with ALL interactions!")


if __name__ == "__main__":
    main()
