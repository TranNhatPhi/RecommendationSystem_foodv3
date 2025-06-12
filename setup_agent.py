#!/usr/bin/env python3
"""
🚀 AI Agent Food Recommendation System Setup Script
This script helps you set up and run the AI Agent Food Recommendation System.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def print_banner():
    """Print a fancy banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║       🤖 AI AGENT FOOD RECOMMENDATION SYSTEM 🍽️              ║
    ║                                                               ║
    ║       Smart Food Recommendations with RAG & Vector DB        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required!")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def check_and_install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True


def setup_database():
    """Initialize the database"""
    print("\n🗄️ Setting up database...")
    try:
        from simple_food_db import main as setup_db
        setup_db()
        print("✅ Database setup completed!")
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n⚙️ Setting up environment configuration...")

    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Google Maps API Configuration (Optional)
# Get your API key from: https://developers.google.com/maps/documentation/places/web-service/get-api-key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_TYPE=simple
DATABASE_PATH=./simple_food_db.sqlite
"""
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("📝 Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")


def test_system():
    """Test the system components"""
    print("\n🧪 Testing system components...")

    # Test database
    try:
        from simple_food_db import SimpleFoodRecommendationDB
        db = SimpleFoodRecommendationDB()
        stats = db.get_collection_stats()
        print(
            f"✅ Database: {stats['recipes_count']} recipes, {stats['customers_count']} customers")
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

    # Test AI agent
    try:
        from food_ai_agent import get_agent_instance
        agent = get_agent_instance()
        response = agent.process_user_request("Test query")
        print("✅ AI Agent: Working properly")
    except Exception as e:
        print(f"❌ AI Agent test failed: {e}")
        return False

    return True


def show_usage_info():
    """Show usage information"""
    print("""
    🎯 SYSTEM READY! Here's how to use it:
    
    1. 🌐 Start the web application:
       python app.py
       
    2. 🔗 Open your browser and go to:
       http://localhost:5000/agent
       
    3. 💬 Start chatting with the AI agent:
       - "Tôi muốn ăn món gì tốt cho sức khỏe?"
       - "Gợi ý món ăn cho người tiểu đường"
       - "Tìm món ăn Việt Nam dễ làm"
    
    📚 Additional resources:
    - API Documentation: http://localhost:5000/api/docs
    - Test Interface: http://localhost:5000/test
    - Main Dashboard: http://localhost:5000/
    
    🔧 Configuration:
    - Edit .env file to add your OpenAI API key for better responses
    - Check AI_AGENT_README.md for detailed documentation
    
    🆘 Need help?
    - Check the logs in the terminal
    - Test APIs with: python test_agent_api.py
    - Review AI_AGENT_README.md for troubleshooting
    """)


def main():
    """Main setup function"""
    print_banner()

    # Check prerequisites
    check_python_version()

    # Install requirements
    if not check_and_install_requirements():
        print("❌ Setup failed at package installation")
        return

    # Setup database
    if not setup_database():
        print("❌ Setup failed at database initialization")
        return

    # Create environment file
    create_env_file()

    # Test system
    if not test_system():
        print("⚠️ Some components failed testing, but system may still work")

    # Show usage info
    show_usage_info()

    print("\n🎉 Setup completed successfully!")
    print("🚀 Ready to start the AI Food Recommendation Agent!")


if __name__ == "__main__":
    main()


def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Successfully installed all requirements")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def setup_vector_database():
    """Setup and populate the vector database"""
    print("🗄️ Setting up vector database...")
    try:
        from populate_chromadb import main as populate_db
        populate_db()
        print("✅ Vector database setup complete")
        return True
    except Exception as e:
        print(f"❌ Error setting up vector database: {e}")
        return False


def setup_environment():
    """Setup environment variables and configuration"""
    print("🔧 Setting up environment...")

    # Create .env file template if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Maps API Configuration (Optional)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)

        print("📝 Created .env file template")
        print("⚠️  Please update the .env file with your API keys")

    return True


def check_data_files():
    """Check if required data files exist"""
    print("📊 Checking data files...")

    required_files = [
        "interactions_enhanced_final.csv",
        "customers_data.csv"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required data files: {missing_files}")
        return False
    else:
        print("✅ All required data files found")
        return True


def main():
    """Main setup function"""
    print("🚀 Setting up Food Recommendation AI Agent System")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)

    # Step 1: Check data files
    if not check_data_files():
        print("⚠️  Some data files are missing. The system may not work correctly.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    # Step 2: Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please check the error messages above.")
        sys.exit(1)

    # Step 3: Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)

    # Step 4: Setup vector database
    print("\n" + "=" * 50)
    print("This may take a few minutes...")
    if not setup_vector_database():
        print("❌ Failed to setup vector database")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your OpenAI API key")
    print("2. Run the application: python app.py")
    print("3. Open your browser and go to: http://localhost:5000/agent")
    print("\n🔗 Available endpoints:")
    print("   • Main App: http://localhost:5000/")
    print("   • AI Agent: http://localhost:5000/agent")
    print("   • API Test: http://localhost:5000/test")
    print("\n💡 Features available:")
    print("   • AI-powered food recommendations")
    print("   • RAG system with vector database")
    print("   • Semantic search for recipes")
    print("   • Personalized nutrition advice")
    print("   • Restaurant location integration")


if __name__ == "__main__":
    main()
