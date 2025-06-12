"""
Setup script cho Enhanced AI Agent
Tự động cài đặt và cấu hình hệ thống
"""

import os
import subprocess
import sys
from pathlib import Path


def install_requirements():
    """Cài đặt requirements"""
    print("🔄 Installing requirements...")
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', 'enhanced_requirements.txt'])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True


def setup_environment():
    """Thiết lập environment variables"""
    print("🔄 Setting up environment...")

    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# Enhanced AI Agent Configuration
# OpenAI API Key (required for GPT-4)
OPENAI_API_KEY=your-openai-api-key-here

# Google Maps API Key (optional, for location features)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_food_db
CHROMA_COLLECTION_SIZE=10000

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Performance Settings
MAX_CONCURRENT_REQUESTS=10
CACHE_SIZE=1000
"""

        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)

        print("✅ Created .env file")
        print("⚠️  Please update .env file with your actual API keys")
    else:
        print("✅ .env file already exists")


def create_directories():
    """Tạo các thư mục cần thiết"""
    print("🔄 Creating directories...")

    directories = [
        './chroma_food_db',
        './logs',
        './cache',
        './temp'
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def test_imports():
    """Test import các modules chính"""
    print("🔄 Testing imports...")

    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError:
        print("❌ ChromaDB import failed")
        return False

    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError:
        print("❌ OpenAI import failed")
        return False

    try:
        import langchain
        print("✅ Langchain imported successfully")
    except ImportError:
        print("❌ Langchain import failed")
        return False

    return True


def initialize_database():
    """Khởi tạo ChromaDB"""
    print("🔄 Initializing ChromaDB...")

    try:
        from enhanced_ai_agent import get_enhanced_agent_instance

        # This will create the ChromaDB collections
        agent = get_enhanced_agent_instance()
        print("✅ ChromaDB initialized successfully")

    except Exception as e:
        print(f"❌ ChromaDB initialization failed: {e}")
        return False

    return True


def run_tests():
    """Chạy tests cơ bản"""
    print("🔄 Running basic tests...")

    try:
        # Test basic functionality
        from enhanced_ai_agent import EnhancedFoodAIAgent

        agent = EnhancedFoodAIAgent()
        print("✅ Enhanced AI Agent created successfully")

        # Test database connections
        if agent.food_collection and agent.customer_collection:
            print("✅ Database collections accessible")
        else:
            print("❌ Database collections not accessible")
            return False

    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

    return True


def main():
    """Main setup function"""
    print("🚀 Enhanced AI Agent Setup")
    print("=" * 50)

    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return

    # Step 2: Setup environment
    setup_environment()

    # Step 3: Create directories
    create_directories()

    # Step 4: Test imports
    if not test_imports():
        print("❌ Setup failed at imports testing")
        return

    # Step 5: Initialize database
    if not initialize_database():
        print("⚠️  Database initialization failed, but setup can continue")

    # Step 6: Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup completed")

    print("\n" + "=" * 50)
    print("🎉 Enhanced AI Agent Setup Complete!")
    print("\nNext steps:")
    print("1. Update .env file with your API keys")
    print("2. Run: python app.py")
    print("3. Visit: http://localhost:5000/ai-agent")
    print("\nFor testing:")
    print("python -c 'from enhanced_ai_agent import test_agent; import asyncio; asyncio.run(test_agent())'")


if __name__ == "__main__":
    main()
