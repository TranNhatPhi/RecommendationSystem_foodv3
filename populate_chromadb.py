import pandas as pd
import chromadb
from chromadb.config import Settings
import os
import uuid
from typing import List, Dict
import numpy as np


class FoodRecommendationVectorDB:
    def __init__(self, persist_directory="./vector_store/chroma_db"):
        """Initialize ChromaDB client and collection"""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Create or get collections with default embedding function
        self.recipes_collection = self.client.get_or_create_collection(
            name="food_recipes",
            metadata={"description": "Food recipes and interactions"}
        )

        self.customers_collection = self.client.get_or_create_collection(
            name="customers",
            metadata={"description": "Customer profiles and preferences"}
        )

    def populate_recipes_collection(self, interactions_file="interactions_enhanced_final.csv"):
        """Populate recipes collection from interactions CSV"""
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

            documents = []
            metadatas = []
            ids = []

            for idx, row in recipe_groups.iterrows():
                # Create document text for embedding
                doc_text = f"""
                Tên món: {row['recipe_name']}
                Độ khó: {row['difficulty']}
                Bữa ăn: {row['meal_time']}
                Loại dinh dưỡng: {row['nutrition_category']}
                Kcal: {row['estimated_calories']}
                Thời gian chuẩn bị: {row['preparation_time_minutes']} phút
                Số nguyên liệu: {row['ingredient_count']}
                Giá ước tính: {row['estimated_price_vnd']} VND
                Đánh giá trung bình: {row['rating']:.2f}
                Bình luận: {row['comment'][:500]}
                """.strip()

                documents.append(doc_text)
                ids.append(f"recipe_{idx}")

                # Metadata for filtering
                metadatas.append({
                    "recipe_name": str(row['recipe_name']),
                    "recipe_url": str(row['recipe_url']),
                    "difficulty": str(row['difficulty']),
                    "meal_time": str(row['meal_time']),
                    "nutrition_category": str(row['nutrition_category']),
                    "estimated_calories": float(row['estimated_calories']) if pd.notna(row['estimated_calories']) else 0,
                    "preparation_time_minutes": float(row['preparation_time_minutes']) if pd.notna(row['preparation_time_minutes']) else 0,
                    "ingredient_count": float(row['ingredient_count']) if pd.notna(row['ingredient_count']) else 0,
                    "estimated_price_vnd": float(row['estimated_price_vnd']) if pd.notna(row['estimated_price_vnd']) else 0,
                    "avg_rating": float(row['rating']) if pd.notna(row['rating']) else 0,
                    "content_score": float(row['content_score']) if pd.notna(row['content_score']) else 0,
                    "cf_score": float(row['cf_score']) if pd.notna(row['cf_score']) else 0
                })

            # Add to collection in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i+batch_size]
                batch_metas = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]

                self.recipes_collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )

            print(
                f"✅ Successfully added {len(documents)} recipes to vector database")

        except Exception as e:
            print(f"❌ Error populating recipes: {str(e)}")

    def populate_customers_collection(self, customers_file="customers_data.csv"):
        """Populate customers collection from customers CSV"""
        try:
            df = pd.read_csv(customers_file)
            print(f"Loading {len(df)} customers from {customers_file}")

            documents = []
            metadatas = []
            ids = []

            for idx, row in df.iterrows():
                # Create document text for customer profile
                doc_text = f"""
                Khách hàng: {row['full_name']}
                ID: {row['customer_id']}
                Giới tính: {row['gender']}
                Nhóm tuổi: {row['age_group']}
                Khu vực: {row['region']}
                Ngày đăng ký: {row['registration_date']}
                """.strip()

                documents.append(doc_text)
                ids.append(f"customer_{row['customer_id']}")

                metadatas.append({
                    "customer_id": str(row['customer_id']),
                    "full_name": str(row['full_name']),
                    "gender": str(row['gender']),
                    "age_group": str(row['age_group']),
                    "region": str(row['region']),
                    "registration_date": str(row['registration_date'])
                })

            # Add to collection
            self.customers_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            print(
                f"✅ Successfully added {len(documents)} customers to vector database")

        except Exception as e:
            print(f"❌ Error populating customers: {str(e)}")

    def search_recipes(self, query: str, filters: Dict = None, n_results: int = 5):
        """Search recipes using semantic similarity"""
        try:
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    if key in ['difficulty', 'meal_time', 'nutrition_category']:
                        where_clause[key] = value
                    elif key in ['max_calories', 'max_time', 'max_price']:
                        # Handle range queries
                        field_name = key.replace(
                            'max_', 'estimated_') + ('_vnd' if 'price' in key else '_minutes' if 'time' in key else '')
                        if field_name == 'estimated_time_minutes':
                            field_name = 'preparation_time_minutes'
                        where_clause[field_name] = {"$lte": value}

            results = self.recipes_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )

            return results
        except Exception as e:
            print(f"❌ Error searching recipes: {str(e)}")
            return None

    def search_customers(self, query: str, filters: Dict = None, n_results: int = 5):
        """Search customers using semantic similarity"""
        try:
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    where_clause[key] = value

            results = self.customers_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )

            return results
        except Exception as e:
            print(f"❌ Error searching customers: {str(e)}")
            return None

    def get_collection_stats(self):
        """Get statistics about the collections"""
        try:
            recipes_count = self.recipes_collection.count()
            customers_count = self.customers_collection.count()

            return {
                "recipes_count": recipes_count,
                "customers_count": customers_count
            }
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}")
            return {"recipes_count": 0, "customers_count": 0}


def main():
    """Main function to populate the vector database"""
    print("🚀 Initializing Food Recommendation Vector Database...")

    # Initialize vector database
    vector_db = FoodRecommendationVectorDB()

    # Populate collections
    print("\n📚 Populating recipes collection...")
    vector_db.populate_recipes_collection()

    print("\n👥 Populating customers collection...")
    vector_db.populate_customers_collection()

    # Show statistics
    print("\n📊 Database Statistics:")
    stats = vector_db.get_collection_stats()
    print(f"Recipes: {stats['recipes_count']}")
    print(f"Customers: {stats['customers_count']}")

    # Test search functionality
    print("\n🔍 Testing search functionality...")
    test_results = vector_db.search_recipes(
        "món ăn Việt Nam truyền thống tốt cho sức khỏe", n_results=3)
    if test_results and test_results['documents']:
        print("Sample search results:")
        for i, (doc, meta) in enumerate(zip(test_results['documents'][0], test_results['metadatas'][0])):
            print(
                f"{i+1}. {meta['recipe_name']} - {meta['nutrition_category']}")

    print("\n✅ Vector database setup complete!")


if __name__ == "__main__":
    main()
