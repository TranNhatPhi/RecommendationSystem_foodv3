# 📚 Vietnamese Food Recommendation System - Swagger API Documentation

## Tổng quan

Hệ thống gợi ý món ăn Việt Nam với API RESTful hoàn chỉnh và tài liệu Swagger tương tác.

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies bổ sung

```bash
pip install -r swagger_requirements.txt
```

Hoặc cài đặt từng package:

```bash
pip install flask-restx==1.3.0
pip install werkzeug==2.3.7
```

### 2. Chạy server với Swagger

```bash
python run_swagger.py
```

### 3. Truy cập tài liệu API

- **Swagger UI tương tác**: http://localhost:5000/swagger/
- **Tài liệu API chi tiết**: http://localhost:5000/api-docs
- **Ứng dụng chính**: http://localhost:5000/

## 📋 API Endpoints

### 🛒 Gợi ý bán kèm (Upsell)

#### 1. Gợi ý combo món ăn
```
GET /api/upsell_combos?user_id={user_id}&item_id={item_id}
```

#### 2. Gợi ý món phụ
```
GET /api/upsell_sides?user_id={user_id}&main_dish_id={main_dish_id}
```

### 👨‍👩‍👧‍👦 Gợi ý gia đình

#### 3. Combo gia đình
```
GET /api/family_combos?user_id={user_id}&family_size={family_size}
```

### 🎂 Gợi ý theo độ tuổi

#### 4. Gợi ý theo nhóm tuổi
```
GET /api/age_based_recommendations?user_id={user_id}&age_group={age_group}
```

Các nhóm tuổi: `children`, `teenagers`, `adults`, `elderly`

### 🍽️ Gợi ý theo bữa ăn

#### 5. Gợi ý theo bữa ăn cụ thể
```
GET /api/meal_recommendations?user_id={user_id}&meal_type={meal_type}&count={count}
```

Loại bữa ăn: `breakfast`, `lunch`, `dinner`

#### 6. Thực đơn hoàn chỉnh (6 menu)
```
GET /api/meal_plans?user_id={user_id}
```

### 🥗 Gợi ý dinh dưỡng

#### 7. Gợi ý theo mục tiêu dinh dưỡng
```
GET /api/nutrition_recommendations?user_id={user_id}&nutrition_type={nutrition_type}&count={count}
```

Loại dinh dưỡng:
- `weight-loss`: Giảm cân
- `balanced`: Cân bằng dinh dưỡng
- `blood-boost`: Bổ máu
- `brain-boost`: Tăng cường trí não
- `digestive-support`: Hỗ trợ tiêu hóa

## 📝 Ví dụ sử dụng

### JavaScript/Fetch
```javascript
// Lấy gợi ý dinh dưỡng giảm cân
const response = await fetch('/api/nutrition_recommendations?user_id=12345&nutrition_type=weight-loss');
const data = await response.json();
console.log(data);

// Lấy combo gia đình 4 người
const familyCombo = await fetch('/api/family_combos?user_id=12345&family_size=4');
const combo = await familyCombo.json();
console.log(combo);
```

### Python/Requests
```python
import requests

# Gợi ý món sáng
response = requests.get('http://localhost:5000/api/meal_recommendations', 
                       params={'user_id': '12345', 'meal_type': 'breakfast'})
data = response.json()
print(data)

# Gợi ý theo độ tuổi trẻ em
response = requests.get('http://localhost:5000/api/age_based_recommendations',
                       params={'user_id': '12345', 'age_group': 'children'})
data = response.json()
print(data)
```

### cURL
```bash
# Gợi ý combo bán kèm
curl -X GET "http://localhost:5000/api/upsell_combos?user_id=12345&item_id=54"

# Gợi ý thực đơn hoàn chỉnh
curl -X GET "http://localhost:5000/api/meal_plans?user_id=12345"
```

## 📊 Response Format

### Thành công (200)
```json
{
  "recommendations": [...],
  "message": "Success message",
  "user_id": "12345"
}
```

### Lỗi (400/500)
```json
{
  "error": "Error message description"
}
```

## 🔧 Tùy chỉnh

### Thêm endpoint mới

1. Sửa file `swagger_docs.py`
2. Thêm namespace và resource class
3. Định nghĩa model cho request/response
4. Thêm documentation với decorators

### Thay đổi cấu hình

Sửa các thông số trong `swagger_docs.py`:
- `title`: Tiêu đề API
- `description`: Mô tả API
- `version`: Phiên bản
- `contact`: Thông tin liên hệ

## 🛠️ Troubleshooting

### Lỗi Import
```
ImportError: No module named 'flask_restx'
```
**Giải pháp**: Cài đặt flask-restx
```bash
pip install flask-restx==1.3.0
```

### Lỗi Werkzeug
```
AttributeError: module 'werkzeug' has no attribute 'cached_property'
```
**Giải pháp**: Downgrade Werkzeug
```bash
pip install werkzeug==2.3.7
```

### Swagger UI không tải
- Kiểm tra port 5000 có bị chiếm không
- Thử truy cập http://127.0.0.1:5000/swagger/ thay vì localhost
- Kiểm tra firewall và antivirus

## 📞 Hỗ trợ

- **GitHub Issues**: Tạo issue để báo lỗi
- **Documentation**: Xem chi tiết tại `/api-docs`
- **Swagger UI**: Test API tại `/swagger/`

## 📄 License

MIT License - Tự do sử dụng cho mục đích học tập và phát triển.

---

💡 **Tip**: Sử dụng Swagger UI để test API trực tiếp trong trình duyệt thay vì viết code test riêng!
