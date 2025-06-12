#!/usr/bin/env python3
"""
Script to load ALL 14,953 interactions into the database
"""

import os
import sys
from simple_food_db import SimpleFoodRecommendationDB
import sqlite3


def main():
    print("🚀 Loading ALL 14,953 interactions into database...")
    print(f"📁 Current directory: {os.getcwd()}")

    # Check if the data file exists
    data_file = "interactions_enhanced_final.csv"
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        # List available CSV files
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        print("Available CSV files:", csv_files)
        return False

    print(f"✅ Found data file: {data_file}")

    # Check current state before loading
    print("\n📊 Current Database State BEFORE loading:")
    db_path = "./simple_food_db.sqlite"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
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

    # Initialize database and load all interactions
    try:
        db = SimpleFoodRecommendationDB()
        print("\n🔥 Starting to load ALL interactions...")
        success = db.populate_all_interactions(data_file)

        if success:
            print("\n🎉 Successfully loaded all interactions!")

            # Check final state
            print("\n📊 Database State AFTER loading:")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM interactions')
            final_interactions_count = cursor.fetchone()[0]
            print(f"Total Interactions: {final_interactions_count}")

            # Show sample data
            cursor.execute(
                'SELECT customer_id, recipe_name, rating FROM interactions LIMIT 5')
            samples = cursor.fetchall()
            print("\n📋 Sample interactions:")
            for i, (customer_id, recipe_name, rating) in enumerate(samples, 1):
                print(
                    f"{i}. Customer {customer_id}: {recipe_name} (Rating: {rating})")

            conn.close()
            return True
        else:
            print("❌ Failed to load interactions")
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All interactions loaded successfully!")
    else:
        print("\n❌ Failed to load interactions")
