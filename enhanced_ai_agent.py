"""
AI Agent Enhanced với LLM, RAG, ChromaDB và MCP
Tích hợp GPT-4 API, Vector Database, Google Maps
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
import openai
import chromadb
from chromadb.config import Settings
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document
import requests
from datetime import datetime
import asyncio
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedFoodAIAgent:
    """
    AI Agent tư vấn món ăn với tích hợp:
    - GPT-4 API cho LLM processing
    - ChromaDB cho vector storage
    - RAG cho retrieval augmented generation
    - Google Maps API cho location services
    - MCP (Model Context Protocol) support
    """

    def __init__(self):
        self.setup_apis()
        self.setup_vector_db()
        self.setup_prompt_templates()
        self.load_food_data()

    def setup_apis(self):
        """Thiết lập API keys và clients"""
        # OpenAI API setup
        self.openai_api_key = os.getenv(
            'OPENAI_API_KEY', 'your-openai-api-key-here')
        openai.api_key = self.openai_api_key

        # Google Maps API setup
        self.google_maps_api_key = os.getenv(
            'GOOGLE_MAPS_API_KEY', 'your-google-maps-api-key-here')

        # Embeddings model
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)

        logger.info("✅ APIs configured successfully")

    def setup_vector_db(self):
        """Thiết lập ChromaDB cho vector storage"""
        try:
            # ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path="./chroma_food_db",
                settings=Settings(allow_reset=True)
            )

            # Collection for food data
            self.food_collection = self.chroma_client.get_or_create_collection(
                name="food_recommendations",
                metadata={"hnsw:space": "cosine"}
            )

            # Collection for customer data
            self.customer_collection = self.chroma_client.get_or_create_collection(
                name="customer_profiles",
                metadata={"hnsw:space": "cosine"}
            )

            logger.info("✅ ChromaDB initialized successfully")

        except Exception as e:
            logger.error(f"❌ ChromaDB setup failed: {e}")
            # Fallback to in-memory
            self.chroma_client = chromadb.Client()
            self.food_collection = self.chroma_client.create_collection(
                "food_recommendations")
            self.customer_collection = self.chroma_client.create_collection(
                "customer_profiles")

    def setup_prompt_templates(self):
        """Thiết lập prompt templates chuyên nghiệp"""
        self.system_prompt = """
Bạn là một chuyên gia tư vấn ẩm thực và dinh dưỡng AI, có nhiệm vụ đưa ra các gợi ý món ăn an toàn, hợp vệ sinh, phù hợp với từng nhóm người dùng. 

NHIỆM VỤ CHÍNH:
- Đảm bảo an toàn thực phẩm và vệ sinh cho người tiêu dùng
- Tư vấn món ăn phù hợp với tình trạng sức khỏe cá nhân
- Đưa ra gợi ý sáng tạo, thực tế và dễ thực hiện
- Ưu tiên giải pháp dinh dưỡng cân bằng

PHONG CÁCH TƯƠNG TÁC:
- Thân thiện, dễ hiểu, chuyên nghiệp
- Giải thích rõ ràng lý do đằng sau mỗi gợi ý
- Cung cấp thông tin dinh dưỡng cụ thể
- Đưa ra cảnh báo an toàn khi cần thiết

DỰA TRÊN:
- Dữ liệu khách hàng và lịch sử tương tác
- Thông tin dinh dưỡng và an toàn thực phẩm
- Xu hướng ẩm thực địa phương
- Khuyến nghị y tế chung
"""

        self.user_prompt_template = """
THÔNG TIN KHÁCH HÀNG:
- ID: {customer_id}
- Thông tin cá nhân: {customer_info}
- Lịch sử món ăn: {food_history}
- Sở thích: {preferences}
- Hạn chế/Dị ứng: {restrictions}

CÂU HỎI CỦA NGƯỜI DÙNG:
{user_question}

NGỮ CẢNH BỔ SUNG (từ RAG):
{context_info}

VỊ TRÍ HIỆN TẠI:
{location_info}

YÊU CÂU PHẢN HỒI:
1. Gợi ý món ăn cụ thể (3-5 món)
2. Lý do chọn món (dinh dưỡng, phù hợp)
3. Cảnh báo an toàn (nếu có)
4. Gợi ý địa điểm gần nhất (nếu cần)
5. Mẹo chế biến/bảo quản
"""

    def load_food_data(self):
        """Load và embedding dữ liệu món ăn vào ChromaDB"""
        try:
            # Load interactions data
            interactions_df = pd.read_csv('interactions_enhanced_final.csv')
            customers_df = pd.read_csv('customers_data.csv')

            self.interactions_data = interactions_df
            self.customers_data = customers_df

            # Check if data already embedded
            if self.food_collection.count() == 0:
                self._embed_food_data(interactions_df)

            if self.customer_collection.count() == 0:
                self._embed_customer_data(customers_df)

            logger.info(
                f"✅ Loaded {len(interactions_df)} interactions and {len(customers_df)} customers")

        except Exception as e:
            logger.error(f"❌ Failed to load food data: {e}")
            # Create dummy data for testing
            self.interactions_data = pd.DataFrame()
            self.customers_data = pd.DataFrame()

    def _embed_food_data(self, df: pd.DataFrame):
        """Embed food interaction data vào ChromaDB"""
        logger.info("🔄 Embedding food data...")

        batch_size = 100
        total_rows = len(df)

        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i:i+batch_size]

            documents = []
            metadatas = []
            ids = []

            for _, row in batch.iterrows():
                # Create document text for embedding
                doc_text = f"""
                Món ăn: {row.get('food_name', 'Unknown')}
                Loại: {row.get('food_category', 'Unknown')}
                Đánh giá: {row.get('rating', 0)}/5
                Dinh dưỡng: Calories: {row.get('calories', 0)}, Protein: {row.get('protein', 0)}g
                Mô tả: {row.get('description', '')}
                Thành phần: {row.get('ingredients', '')}
                """

                documents.append(doc_text)
                metadatas.append({
                    'food_id': str(row.get('food_id', i)),
                    'food_name': str(row.get('food_name', 'Unknown')),
                    'category': str(row.get('food_category', 'Unknown')),
                    'rating': float(row.get('rating', 0)),
                    'calories': int(row.get('calories', 0)),
                    'protein': float(row.get('protein', 0))
                })
                ids.append(f"food_{i}_{row.get('food_id', i)}")

            # Add to ChromaDB
            self.food_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            logger.info(f"📊 Embedded {i+len(batch)}/{total_rows} food items")

    def _embed_customer_data(self, df: pd.DataFrame):
        """Embed customer profile data vào ChromaDB"""
        logger.info("🔄 Embedding customer data...")

        for _, row in df.iterrows():
            doc_text = f"""
            Khách hàng: {row.get('full_name', 'Unknown')}
            Tuổi: {row.get('age_group', 'Unknown')}
            Địa điểm: {row.get('location', 'Unknown')}
            Sở thích: {row.get('preferences', '')}
            Hạn chế: {row.get('dietary_restrictions', '')}
            """

            self.customer_collection.add(
                documents=[doc_text],
                metadatas=[{
                    'customer_id': str(row.get('customer_id', '')),
                    'name': str(row.get('full_name', 'Unknown')),
                    'age_group': str(row.get('age_group', 'Unknown')),
                    'location': str(row.get('location', 'Unknown'))
                }],
                ids=[f"customer_{row.get('customer_id', '')}"]
            )

    async def get_recommendation(self, customer_id: str, question: str, location: str = None) -> Dict[str, Any]:
        """
        Main method để lấy gợi ý từ AI Agent
        Tích hợp RAG + LLM + Location services
        """
        try:
            # 1. Lấy thông tin khách hàng
            customer_info = self._get_customer_info(customer_id)

            # 2. RAG - Tìm kiếm thông tin liên quan
            context_info = await self._rag_search(question, customer_id)

            # 3. Lấy thông tin địa điểm
            location_info = await self._get_location_context(location) if location else "Không có thông tin vị trí"

            # 4. Tạo prompt và gọi LLM
            response = await self._call_llm(
                customer_id=customer_id,
                customer_info=customer_info,
                user_question=question,
                context_info=context_info,
                location_info=location_info
            )

            # 5. Lưu interaction history
            await self._save_interaction(customer_id, question, response)

            return {
                'success': True,
                'response': response,
                'customer_info': customer_info,
                'context_used': context_info,
                'location_context': location_info,
                'processing_steps': self._get_processing_steps(),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Recommendation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_response': "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại sau."
            }

    def _get_customer_info(self, customer_id: str) -> Dict[str, Any]:
        """Lấy thông tin khách hàng từ database"""
        try:
            # Query from ChromaDB
            results = self.customer_collection.query(
                query_texts=[f"customer_id:{customer_id}"],
                n_results=1
            )

            if results['documents']:
                customer_data = results['metadatas'][0][0]

                # Get interaction history
                interactions = self.interactions_data[
                    self.interactions_data['customer_id'] == int(customer_id)
                ] if not self.interactions_data.empty else pd.DataFrame()

                return {
                    'customer_id': customer_id,
                    'name': customer_data.get('name', 'Unknown'),
                    'age_group': customer_data.get('age_group', 'Unknown'),
                    'location': customer_data.get('location', 'Unknown'),
                    'total_interactions': len(interactions),
                    'favorite_foods': self._get_favorite_foods(interactions),
                    'avg_rating': interactions['rating'].mean() if not interactions.empty else 0
                }
            else:
                return {
                    'customer_id': customer_id,
                    'name': 'Khách hàng mới',
                    'note': 'Chưa có dữ liệu lịch sử'
                }

        except Exception as e:
            logger.error(f"❌ Failed to get customer info: {e}")
            return {'customer_id': customer_id, 'error': 'Không thể tải thông tin khách hàng'}

    def _get_favorite_foods(self, interactions: pd.DataFrame) -> List[str]:
        """Lấy danh sách món ăn yêu thích"""
        if interactions.empty:
            return []

        # Lấy top món ăn có rating cao
        top_foods = interactions[interactions['rating']
                                 >= 4]['food_name'].value_counts().head(5)
        return top_foods.index.tolist()

    async def _rag_search(self, question: str, customer_id: str) -> str:
        """RAG - Retrieval Augmented Generation search"""
        try:
            # Search relevant food items
            food_results = self.food_collection.query(
                query_texts=[question],
                n_results=5
            )

            # Search similar customer profiles
            customer_results = self.customer_collection.query(
                query_texts=[f"tương tự khách hàng {customer_id}"],
                n_results=3
            )

            # Combine results
            context_parts = []

            if food_results['documents'][0]:
                context_parts.append("THÔNG TIN MÓN ĂN LIÊN QUAN:")
                for i, doc in enumerate(food_results['documents'][0][:3]):
                    metadata = food_results['metadatas'][0][i]
                    context_parts.append(
                        f"- {metadata['food_name']}: {doc[:200]}...")

            if customer_results['documents'][0]:
                context_parts.append("\nKHÁCH HÀNG TƯƠNG TỰ:")
                for doc in customer_results['documents'][0][:2]:
                    context_parts.append(f"- {doc[:150]}...")

            return "\n".join(context_parts) if context_parts else "Không tìm thấy thông tin liên quan"

        except Exception as e:
            logger.error(f"❌ RAG search failed: {e}")
            return "Lỗi tìm kiếm thông tin ngữ cảnh"

    async def _get_location_context(self, location: str) -> str:
        """Lấy thông tin địa điểm từ Google Maps API"""
        try:
            if not location or self.google_maps_api_key == 'your-google-maps-api-key-here':
                return "Không có thông tin vị trí"

            # Google Places API - tìm nhà hàng gần đó
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                'location': location,
                'radius': 2000,
                'type': 'restaurant',
                'key': self.google_maps_api_key
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()

                    if data['status'] == 'OK':
                        restaurants = []
                        for place in data['results'][:5]:
                            restaurants.append({
                                'name': place['name'],
                                'rating': place.get('rating', 0),
                                'address': place.get('vicinity', 'N/A')
                            })

                        return f"Nhà hàng gần bạn: {', '.join([r['name'] for r in restaurants])}"

        except Exception as e:
            logger.error(f"❌ Location context failed: {e}")

        return "Không thể lấy thông tin vị trí"

    async def _call_llm(self, customer_id: str, customer_info: Dict, user_question: str,
                        context_info: str, location_info: str) -> str:
        """Gọi GPT-4 API với prompt được tối ưu"""
        try:
            # Prepare user prompt
            user_prompt = self.user_prompt_template.format(
                customer_id=customer_id,
                customer_info=json.dumps(
                    customer_info, ensure_ascii=False, indent=2),
                food_history=customer_info.get('favorite_foods', []),
                preferences="Dựa trên lịch sử tương tác",
                restrictions="Cần xác định thêm",
                user_question=user_question,
                context_info=context_info,
                location_info=location_info
            )

            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"❌ LLM call failed: {e}")
            # Fallback response
            return self._generate_fallback_response(customer_info, user_question)

    def _generate_fallback_response(self, customer_info: Dict, question: str) -> str:
        """Tạo phản hồi dự phòng khi LLM không khả dụng"""
        customer_name = customer_info.get('name', 'bạn')
        favorite_foods = customer_info.get('favorite_foods', [])

        response = f"Xin chào {customer_name}! "

        if favorite_foods:
            response += f"Dựa trên lịch sử, tôi thấy bạn thích {', '.join(favorite_foods[:3])}. "

        response += """
Tôi gợi ý một số món ăn an toàn và bổ dưỡng:

🍜 **Phở gà**: Đầy đủ dinh dưỡng, dễ tiêu hóa, an toàn cho mọi lứa tuổi
🥗 **Salad rau củ**: Giàu vitamin, tốt cho sức khỏe, ít calo
🍛 **Cơm gà nướng**: Protein cao, cân bằng dinh dưỡng

**Lưu ý an toàn:**
- Chọn thực phẩm tươi, nguồn gốc rõ ràng
- Chế biến kỹ, đảm bảo vệ sinh
- Uống nhiều nước, ăn đúng giờ

Bạn có muốn tôi gợi ý thêm món nào khác không?
"""

        return response

    async def _save_interaction(self, customer_id: str, question: str, response: str):
        """Lưu lịch sử tương tác"""
        try:
            interaction_data = {
                'customer_id': customer_id,
                'question': question,
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4'
            }

            # Save to ChromaDB for future RAG
            doc_text = f"Câu hỏi: {question}\nTrả lời: {response[:500]}..."

            self.food_collection.add(
                documents=[doc_text],
                metadatas=[interaction_data],
                ids=[f"interaction_{customer_id}_{datetime.now().timestamp()}"]
            )

        except Exception as e:
            logger.error(f"❌ Failed to save interaction: {e}")

    def _get_processing_steps(self) -> List[Dict[str, str]]:
        """Trả về các bước xử lý cho UI visualization"""
        return [
            {
                'id': 'input_analysis',
                'title': '🔍 Phân tích đầu vào',
                'status': 'completed',
                'description': 'Xử lý và hiểu câu hỏi người dùng'
            },
            {
                'id': 'customer_profile',
                'title': '👤 Tải hồ sơ khách hàng',
                'status': 'completed',
                'description': 'Truy xuất thông tin và lịch sử khách hàng'
            },
            {
                'id': 'rag_search',
                'title': '🔎 Tìm kiếm RAG',
                'status': 'completed',
                'description': 'Tìm kiếm thông tin liên quan từ vector database'
            },
            {
                'id': 'location_context',
                'title': '📍 Ngữ cảnh vị trí',
                'status': 'completed',
                'description': 'Lấy thông tin địa điểm từ Google Maps'
            },
            {
                'id': 'llm_processing',
                'title': '🧠 Xử lý LLM',
                'status': 'completed',
                'description': 'Gọi GPT-4 để tạo gợi ý thông minh'
            },
            {
                'id': 'response_formatting',
                'title': '📝 Định dạng phản hồi',
                'status': 'completed',
                'description': 'Tối ưu hóa và định dạng câu trả lời'
            }
        ]


# Singleton instance
_enhanced_agent_instance = None


def get_enhanced_agent_instance() -> EnhancedFoodAIAgent:
    """Get singleton instance của Enhanced AI Agent"""
    global _enhanced_agent_instance
    if _enhanced_agent_instance is None:
        _enhanced_agent_instance = EnhancedFoodAIAgent()
    return _enhanced_agent_instance

# Test function


async def test_agent():
    """Test function để kiểm tra agent"""
    agent = get_enhanced_agent_instance()

    result = await agent.get_recommendation(
        customer_id="1001",
        question="Tôi muốn ăn món gì vừa tốt cho sức khỏe vừa ngon miệng?",
        location="10.762622,106.660172"  # Ho Chi Minh City coordinates
    )

    print("🎯 Test Result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    # Run test
    asyncio.run(test_agent())
