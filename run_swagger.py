#!/usr/bin/env python3
"""
Vietnamese Food Recommendation System - Swagger Server
Run this to start the server with Swagger documentation
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from swagger_docs import app

    print("🚀 Starting Vietnamese Food Recommendation System with Swagger Documentation...")
    print("📚 Swagger UI: http://localhost:5000/swagger/")
    print("📄 API Docs: http://localhost:5000/api-docs")
    print("🏠 Main App: http://localhost:5000/")
    print("🔄 Press Ctrl+C to stop the server")

    # Add route for API documentation page
    @app.route('/api-docs')
    def api_docs():
        from flask import render_template
        return render_template('api_docs.html')

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

except ImportError as e:
    print(f"❌ Error importing swagger_docs: {e}")
    print("💡 Please install required packages:")
    print("   pip install flask-restx werkzeug==2.3.7")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)
