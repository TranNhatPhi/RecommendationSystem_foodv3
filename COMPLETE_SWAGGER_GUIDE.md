# 🍽️ Vietnamese Food Recommendation System - Complete Swagger API Documentation

## 📋 Tổng quan hệ thống

Hệ thống gợi ý món ăn Việt Nam được xây dựng với Flask và Machine Learning, cung cấp API RESTful hoàn chỉnh với tài liệu Swagger tương tác.

### 🎯 Mục tiêu
- Gợi ý món ăn thông minh dựa trên machine learning
- API RESTful dễ sử dụng và tích hợp
- Tài liệu API chi tiết với Swagger UI
- Hỗ trợ nhiều loại gợi ý khác nhau

## 🚀 Khởi chạy hệ thống

### 1. Cài đặt dependencies
```bash
# Cài đặt packages cơ bản
pip install -r requirements.txt

# Cài đặt packages cho Swagger
pip install -r swagger_requirements.txt
```

### 2. Chạy server với Swagger
```bash
python run_swagger.py
```

### 3. Truy cập các trang
- **Swagger UI**: http://localhost:5000/swagger/
- **API Documentation**: http://localhost:5000/api-docs  
- **Main Application**: http://localhost:5000/
- **API Tester**: test_swagger_endpoints.html

## 📚 Tài liệu API chi tiết

### 🔗 Base URL
```
http://localhost:5000/api/
```

### 📊 Response Format

#### Thành công (200 OK)
```json
{
  "recommendations": [...],
  "message": "Success",
  "user_id": "12345"
}
```

#### Lỗi (400/500)
```json
{
  "error": "Error message description"
}
```

## 🛒 1. Upsell APIs - Gợi ý bán kèm

### 1.1 Gợi ý combo món ăn
**Endpoint**: `GET /api/upsell_combos`

**Mô tả**: Gợi ý các combo món ăn để tăng doanh thu

**Tham số**:
- `user_id` (required): ID khách hàng
- `item_id` (required): ID món ăn hiện tại

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/upsell_combos?user_id=12345&item_id=54"
```

**Response**:
```json
{
  "combo_recommendations": [
    {
      "recipe_name": "Phở bò",
      "recipe_url": "https://example.com/pho-bo",
      "combo_discount": "10%",
      "combo_price": "150,000 VND",
      "predicted_rating": 4.5
    }
  ],
  "message": "These items are frequently ordered together"
}
```

### 1.2 Gợi ý món phụ
**Endpoint**: `GET /api/upsell_sides`

**Mô tả**: Gợi ý các món phụ đi kèm với món chính

**Tham số**:
- `user_id` (required): ID khách hàng  
- `main_dish_id` (required): ID món chính

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/upsell_sides?user_id=12345&main_dish_id=54"
```

## 👨‍👩‍👧‍👦 2. Family APIs - Gợi ý gia đình

### 2.1 Combo gia đình
**Endpoint**: `GET /api/family_combos`

**Mô tả**: Tạo combo món ăn hoàn chỉnh cho gia đình

**Tham số**:
- `user_id` (required): ID khách hàng
- `family_size` (optional, default=4): Số người trong gia đình

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/family_combos?user_id=12345&family_size=6"
```

**Response**:
```json
{
  "family_combo": {
    "main_dishes": [...],
    "side_dishes": [...], 
    "desserts": [...]
  },
  "total_price": "900000 VND",
  "preparation_time": "45 minutes",
  "suitable_for": "Family of 6"
}
```

## 🎂 3. Age-based APIs - Gợi ý theo độ tuổi

### 3.1 Gợi ý theo nhóm tuổi
**Endpoint**: `GET /api/age_based_recommendations`

**Mô tả**: Gợi ý món ăn phù hợp với từng nhóm tuổi

**Tham số**:
- `user_id` (required): ID khách hàng
- `age_group` (required): Nhóm tuổi
  - `children`: Trẻ em
  - `teenagers`: Thanh thiếu niên  
  - `adults`: Người lớn
  - `elderly`: Người cao tuổi

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/age_based_recommendations?user_id=12345&age_group=children"
```

**Response**:
```json
{
  "age_group": "children",
  "recommendations": [...],
  "nutrition_focus": "Growth, brain development, bone strength"
}
```

## 🍽️ 4. Meal APIs - Gợi ý theo bữa ăn

### 4.1 Gợi ý theo bữa ăn cụ thể
**Endpoint**: `GET /api/meal_recommendations`

**Mô tả**: Gợi ý món ăn cho từng bữa (sáng, trưa, tối)

**Tham số**:
- `user_id` (required): ID khách hàng
- `meal_type` (required): Loại bữa ăn
  - `breakfast`: Bữa sáng
  - `lunch`: Bữa trưa
  - `dinner`: Bữa tối
- `count` (optional, default=6): Số lượng gợi ý (1-20)

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/meal_recommendations?user_id=12345&meal_type=breakfast&count=5"
```

### 4.2 Thực đơn hoàn chỉnh
**Endpoint**: `GET /api/meal_plans`

**Mô tả**: Tạo 6 thực đơn hoàn chỉnh với đầy đủ bữa sáng, trưa, tối

**Tham số**:
- `user_id` (required): ID khách hàng

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/meal_plans?user_id=12345"
```

**Response**:
```json
{
  "user_id": "12345",
  "meal_plans": [
    {
      "menu_number": 1,
      "breakfast": {...},
      "lunch": {...},
      "dinner": {...}
    },
    ...
  ]
}
```

## 🥗 5. Nutrition APIs - Gợi ý dinh dưỡng

### 5.1 Gợi ý theo mục tiêu dinh dưỡng
**Endpoint**: `GET /api/nutrition_recommendations`

**Mô tả**: Gợi ý món ăn theo mục tiêu dinh dưỡng cụ thể

**Tham số**:
- `user_id` (required): ID khách hàng
- `nutrition_type` (required): Loại dinh dưỡng
  - `weight-loss`: Giảm cân
  - `balanced`: Cân bằng dinh dưỡng
  - `blood-boost`: Bổ máu
  - `brain-boost`: Tăng cường trí não
  - `digestive-support`: Hỗ trợ tiêu hóa
- `count` (optional, default=6): Số lượng gợi ý (1-20)

**Ví dụ**:
```bash
curl -X GET "http://localhost:5000/api/nutrition_recommendations?user_id=12345&nutrition_type=weight-loss&count=10"
```

**Response**:
```json
{
  "nutrition_type": "weight-loss",
  "recommendations": [
    {
      "recipe_name": "Gỏi cuốn tôm thịt",
      "recipe_url": "https://example.com/goi-cuon",
      "difficulty": "Dễ",
      "meal_time": "lunch",
      "predicted_rating": 4.2,
      "item_index": 123,
      "estimated_calories": 180,
      "preparation_time_minutes": 20,
      "ingredient_count": 8,
      "estimated_price_vnd": 45000
    }
  ],
  "nutrition_focus": "Giảm cân, ít chất béo, nhiều chất xơ, protein nạc",
  "user_id": "12345"
}
```

## 🧪 Testing & Debugging

### 1. Swagger UI (Recommended)
Truy cập http://localhost:5000/swagger/ để:
- Xem tất cả endpoints
- Test API trực tiếp trong browser
- Xem request/response examples
- Validate parameters

### 2. API Test Page
Mở file `test_swagger_endpoints.html` để:
- Test tất cả endpoints với UI thân thiện
- Xem response real-time
- Thay đổi parameters dễ dàng

### 3. Command Line Testing
```bash
# Test upsell combos
curl -X GET "http://localhost:5000/api/upsell_combos?user_id=12345&item_id=54"

# Test family combos
curl -X GET "http://localhost:5000/api/family_combos?user_id=12345&family_size=4"

# Test nutrition recommendations
curl -X GET "http://localhost:5000/api/nutrition_recommendations?user_id=12345&nutrition_type=balanced"
```

### 4. JavaScript/Fetch
```javascript
// Example: Get nutrition recommendations
async function getNutritionRecommendations() {
    try {
        const response = await fetch('/api/nutrition_recommendations?user_id=12345&nutrition_type=weight-loss');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### 5. Python/Requests
```python
import requests

# Example: Get meal plans
response = requests.get('http://localhost:5000/api/meal_plans', 
                       params={'user_id': '12345'})
data = response.json()
print(data)
```

## 🔧 Customization & Extension

### 1. Thêm endpoint mới
1. Edit `swagger_docs.py`
2. Tạo namespace mới hoặc sử dụng namespace hiện có
3. Định nghĩa model cho request/response
4. Thêm resource class với documentation

### 2. Thay đổi cấu hình
Trong `swagger_docs.py`:
```python
api = Api(
    app,
    version='2.0',  # Update version
    title='Your Custom Title',  # Update title
    description='Your custom description',  # Update description
    doc='/docs/',  # Change Swagger UI path
)
```

### 3. Thêm authentication
```python
# Add API key authentication
@api.doc(security='apikey')
@api.header('X-API-Key', 'API Key', required=True)
class ProtectedResource(Resource):
    def get(self):
        # Check API key logic
        pass
```

## 🚨 Troubleshooting

### Lỗi thường gặp

#### 1. ImportError: No module named 'flask_restx'
```bash
pip install flask-restx==1.3.0
```

#### 2. AttributeError: module 'werkzeug'
```bash
pip install werkzeug==2.3.7
```

#### 3. Swagger UI không tải
- Kiểm tra port 5000 có bị chiếm không
- Thử http://127.0.0.1:5000/swagger/ thay vì localhost
- Disable firewall/antivirus tạm thời

#### 4. API trả về lỗi 500
- Kiểm tra file `interactions_enhanced_final.csv` có tồn tại không
- Kiểm tra model file `catboost_best_model.cbm`
- Xem log chi tiết trong terminal

#### 5. Customer ID không hợp lệ
- Sử dụng ID từ dataset (1-300)
- Kiểm tra list customer_ids trong code

## 📁 File Structure

```
RecommendationSystemv5/
├── swagger_docs.py              # Main Swagger application
├── run_swagger.py               # Run script with Swagger
├── export_swagger.py            # Export Swagger spec to JSON
├── test_swagger_endpoints.html  # API testing page
├── swagger_requirements.txt     # Swagger dependencies
├── SWAGGER_README.md           # This documentation
├── templates/
│   └── api_docs.html           # API documentation page
└── static/
    └── ...                     # Static files
```

## 🔗 Useful Links

- **Swagger UI**: http://localhost:5000/swagger/
- **API Docs**: http://localhost:5000/api-docs
- **Main App**: http://localhost:5000/
- **Test Page**: test_swagger_endpoints.html
- **Flask-RESTX Docs**: https://flask-restx.readthedocs.io/

## 📞 Support & Contribution

### Getting Help
1. Check this documentation first
2. Test với Swagger UI
3. Xem log trong terminal
4. Create GitHub issue nếu cần

### Contributing
1. Fork repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📝 License

MIT License - Free to use for educational and commercial purposes.

---

## 📊 API Statistics

- **Total Endpoints**: 7
- **Supported Methods**: GET
- **Response Format**: JSON
- **Authentication**: None (can be added)
- **Rate Limiting**: None (can be added)
- **Documentation**: Swagger/OpenAPI 3.0

## 🎉 Conclusion

Hệ thống Swagger API Documentation cung cấp:

✅ **Interactive Documentation**: Swagger UI để test API  
✅ **Complete Coverage**: Tất cả endpoints đều có docs  
✅ **Real Examples**: Request/response examples thực tế  
✅ **Easy Testing**: Multiple ways to test APIs  
✅ **Professional**: Ready for production use  

**Happy Coding! 🚀**
