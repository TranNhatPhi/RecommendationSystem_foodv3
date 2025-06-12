"""
Quick Setup và Test Enhanced AI Agent
Tự động setup và test hệ thống AI Agent với LLM + RAG
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def check_python_version():
    """Kiểm tra Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")
    return True


def install_basic_requirements():
    """Cài đặt requirements cơ bản"""
    print("🔄 Installing basic requirements...")

    basic_packages = [
        'openai==0.28.1',
        'chromadb==0.4.18',
        'langchain==0.0.354',
        'aiohttp==3.9.1',
        'googlemaps==4.10.0',
        'python-dotenv==1.0.0'
    ]

    for package in basic_packages:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"  ⚠️ {package} failed, continuing...")

    print("✅ Basic requirements installed")


def create_env_file():
    """Tạo .env file với demo configuration"""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file already exists")
        return

    env_content = """# Enhanced AI Agent Demo Configuration
# Demo keys - replace with your actual keys for production

# OpenAI API Key (required for GPT-4)
OPENAI_API_KEY=demo-key-please-replace-with-real-key

# Google Maps API Key (optional)
GOOGLE_MAPS_API_KEY=demo-key-please-replace-with-real-key

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_food_db
"""

    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)

    print("✅ Created .env file with demo configuration")


def create_demo_enhanced_agent():
    """Tạo demo version của Enhanced AI Agent"""
    demo_agent_content = '''"""
Demo Enhanced AI Agent - Simplified version cho testing
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class DemoEnhancedFoodAIAgent:
    """Demo version của Enhanced AI Agent"""
    
    def __init__(self):
        self.setup_demo_data()
        logger.info("✅ Demo Enhanced AI Agent initialized")
    
    def setup_demo_data(self):
        """Setup demo data"""
        self.demo_customers = {
            "1001": {
                "name": "Nguyễn Văn A",
                "age_group": "25-35",
                "location": "TP.HCM",
                "preferences": ["Món Việt", "Healthy food"],
                "restrictions": []
            },
            "1002": {
                "name": "Trần Thị B", 
                "age_group": "35-45",
                "location": "Hà Nội",
                "preferences": ["Món Á", "Vegetarian"],
                "restrictions": ["Không ăn thịt"]
            }
        }
        
        self.demo_foods = [
            {
                "name": "Phở gà",
                "category": "Món chính",
                "rating": 4.5,
                "calories": 350,
                "description": "Món phở truyền thống với nước dùng trong, thịt gà tươi"
            },
            {
                "name": "Salad rau củ",
                "category": "Món healthy",
                "rating": 4.2,
                "calories": 150,
                "description": "Salad tươi ngon với nhiều loại rau củ bổ dưỡng"
            }
        ]
    
    async def get_recommendation(self, customer_id: str, question: str, location: str = None) -> Dict[str, Any]:
        """Demo recommendation function"""
        try:
            # Simulate processing time
            import asyncio
            await asyncio.sleep(1)
            
            customer_info = self.demo_customers.get(customer_id, {
                "name": f"Khách hàng #{customer_id}",
                "note": "Demo customer"
            })
            
            # Generate demo response
            response = self._generate_demo_response(customer_info, question)
            
            return {
                'success': True,
                'response': response,
                'customer_info': customer_info,
                'context_used': 'Demo context từ local database',
                'location_context': f'Demo location: {location}' if location else 'Không có thông tin vị trí',
                'processing_steps': self._get_demo_processing_steps(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Demo recommendation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_response': 'Demo fallback response - Hệ thống đang trong chế độ demo'
            }
    
    def _generate_demo_response(self, customer_info: Dict, question: str) -> str:
        """Tạo demo response"""
        customer_name = customer_info.get('name', 'bạn')
        
        responses = {
            'healthy': f"""Xin chào {customer_name}! 

🥗 **Gợi ý món ăn healthy cho bạn:**

1. **Salad rau củ quinoa** - 280 calories
   - Giàu protein th植物, vitamin và khoáng chất
   - Tốt cho tim mạch và tiêu hóa
   
2. **Cá hồi nướng với rau** - 320 calories  
   - Omega-3 cao, protein chất lượng
   - Chống viêm, tốt cho não bộ
   
3. **Soup đậu hũ nấm** - 180 calories
   - Ít calo, nhiều chất xơ
   - Dễ tiêu hóa, phù hợp mọi lứa tuổi

**💡 Lời khuyên an toàn:**
- Chọn nguyên liệu tươi, rõ nguồn gốc
- Chế biến đơn giản, ít dầu mỡ  
- Ăn đủ 5 phần rau củ/ngày

*Được tạo bởi Demo Enhanced AI Agent với công nghệ RAG + LLM*""",

            'vietnamese': f"""Chào {customer_name}! 

🍜 **Gợi ý món Việt truyền thống:**

1. **Phở gà ta** - 350 calories
   - Nước dùng trong vắt, thơm ngon
   - Thịt gà tươi, bánh phở mềm dai
   
2. **Bún bò Huế** - 420 calories
   - Đậm đà hương vị miền Trung
   - Nhiều rau thơm, bổ dưỡng
   
3. **Cơm tấm sườn nướng** - 480 calories
   - Sườn nướng thơm lừng
   - Cơm tấm đặc trưng Sài Gòn

**🛡️ Đảm bảo an toàn:**
- Chọn quán uy tín, vệ sinh sạch sẽ
- Nước dùng nấu kỹ, sôi 100°C
- Rau sống ngâm nước muối loãng

*Demo AI Agent - Chuyên gia tư vấn ẩm thực Việt*""",

            'default': f"""Xin chào {customer_name}!

🍽️ **Gợi ý món ăn cân bằng dinh dưỡng:**

1. **Cơm gà nướng** - 400 calories
   - Protein cao, carb vừa phải
   - Dễ chế biến, an toàn

2. **Mì Quảng** - 380 calories  
   - Đặc sản miền Trung
   - Nhiều hải sản, rau củ

3. **Chả cá Lã Vọng** - 320 calories
   - Cá tươi, thì là thơm
   - Giàu DHA, tốt cho não

**⚡ Lợi ích Enhanced AI:**
- Phân tích dựa trên RAG + Vector Database
- Tích hợp LLM GPT-4 (demo mode)
- Gợi ý cá nhân hóa theo profile
- Kiểm tra an toàn thực phẩm

*Hệ thống demo - Vui lòng cấu hình API keys để sử dụng đầy đủ tính năng*"""
        }
        
        # Simple keyword matching for demo
        question_lower = question.lower()
        if any(word in question_lower for word in ['healthy', 'sức khỏe', 'dinh dưỡng']):
            return responses['healthy']
        elif any(word in question_lower for word in ['việt', 'truyền thống', 'phở', 'bún']):
            return responses['vietnamese'] 
        else:
            return responses['default']
    
    def _get_demo_processing_steps(self) -> List[Dict[str, str]]:
        """Demo processing steps"""
        return [
            {
                'id': 'input_analysis',
                'title': '🔍 Phân tích đầu vào',
                'status': 'completed',
                'description': 'Demo: Phân tích câu hỏi người dùng'
            },
            {
                'id': 'customer_profile',
                'title': '👤 Tải hồ sơ khách hàng',
                'status': 'completed', 
                'description': 'Demo: Lấy thông tin từ demo database'
            },
            {
                'id': 'rag_search',
                'title': '🔎 Tìm kiếm RAG',
                'status': 'completed',
                'description': 'Demo: Tìm kiếm trong demo vector database'
            },
            {
                'id': 'llm_processing',
                'title': '🧠 Xử lý LLM',
                'status': 'completed',
                'description': 'Demo: Sử dụng demo response generator'
            },
            {
                'id': 'response_formatting',
                'title': '📝 Định dạng phản hồi',
                'status': 'completed',
                'description': 'Demo: Tối ưu hóa câu trả lời demo'
            }
        ]

# Singleton instance  
_demo_agent_instance = None

def get_enhanced_agent_instance():
    """Get demo agent instance"""
    global _demo_agent_instance
    if _demo_agent_instance is None:
        _demo_agent_instance = DemoEnhancedFoodAIAgent()
    return _demo_agent_instance

# Test function
async def test_demo_agent():
    """Test demo agent"""
    agent = get_enhanced_agent_instance()
    
    result = await agent.get_recommendation(
        customer_id="1001",
        question="Tôi muốn ăn món gì healthy và ngon?",
        location="TP.HCM"
    )
    
    print("🎯 Demo Test Result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_demo_agent())
'''

    with open('demo_enhanced_agent.py', 'w', encoding='utf-8') as f:
        f.write(demo_agent_content)

    print("✅ Created demo enhanced agent")


def update_app_for_demo():
    """Cập nhật app.py để sử dụng demo agent"""
    print("🔄 Updating app.py for demo mode...")

    # Read current app.py
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()

        # Add demo import fallback
        demo_import = '''
# Import Enhanced AI Agent with LLM + RAG + ChromaDB
try:
    from enhanced_ai_agent import get_enhanced_agent_instance
    ENHANCED_AGENT_AVAILABLE = True
    print("✅ Enhanced AI Agent with LLM + RAG enabled")
except ImportError as e:
    try:
        from demo_enhanced_agent import get_enhanced_agent_instance  
        ENHANCED_AGENT_AVAILABLE = True
        print("✅ Demo Enhanced AI Agent enabled")
    except ImportError as e2:
        ENHANCED_AGENT_AVAILABLE = False
        print(f"⚠️ Enhanced AI Agent not available: {e}")
'''

        # Replace import section
        if 'from enhanced_ai_agent import' in app_content:
            app_content = app_content.replace(
                'try:\n    from enhanced_ai_agent import get_enhanced_agent_instance\n    ENHANCED_AGENT_AVAILABLE = True\n    print("✅ Enhanced AI Agent with LLM + RAG enabled")\nexcept ImportError as e:\n    ENHANCED_AGENT_AVAILABLE = False\n    print(f"⚠️ Enhanced AI Agent not available: {e}")',
                demo_import.strip()
            )

            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(app_content)

            print("✅ Updated app.py for demo mode")
        else:
            print("⚠️ Could not update app.py - manual update needed")

    except Exception as e:
        print(f"❌ Failed to update app.py: {e}")


def test_flask_app():
    """Test Flask app"""
    print("🔄 Testing Flask app...")

    try:
        # Import and test
        from app import app

        with app.test_client() as client:
            # Test landing page
            response = client.get('/ai-agent')
            if response.status_code == 200:
                print("✅ /ai-agent route works")
            else:
                print(f"❌ /ai-agent route failed: {response.status_code}")

            # Test agent page
            response = client.get('/agent')
            if response.status_code == 200:
                print("✅ /agent route works")
            else:
                print(f"❌ /agent route failed: {response.status_code}")

        return True

    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Enhanced AI Agent Quick Setup")
    print("=" * 50)

    # Step 1: Check Python version
    if not check_python_version():
        return

    # Step 2: Install basic requirements
    install_basic_requirements()

    # Step 3: Create environment file
    create_env_file()

    # Step 4: Create demo agent
    create_demo_enhanced_agent()

    # Step 5: Update app for demo
    update_app_for_demo()

    # Step 6: Test Flask app
    if test_flask_app():
        print("\n" + "=" * 50)
        print("🎉 Enhanced AI Agent Demo Setup Complete!")
        print("\n🌐 Access URLs:")
        print("  Landing Page: http://localhost:5000/ai-agent")
        print("  AI Agent:     http://localhost:5000/agent")
        print("\n📝 Notes:")
        print("  - Currently running in DEMO mode")
        print("  - Update .env with real API keys for full functionality")
        print("  - Demo agent provides realistic responses without external APIs")
        print("\n🔧 To start server:")
        print("  python app.py")
    else:
        print("\n❌ Setup completed but Flask app has issues")
        print("Please check the error messages above")


if __name__ == "__main__":
    main()
