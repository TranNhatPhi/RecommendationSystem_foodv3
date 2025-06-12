#!/usr/bin/env python3
"""
Simplified Ultra Analysis App
Clean implementation without conflicts
"""

from flask import Flask, request, jsonify, render_template
import json
import time
import random

app = Flask(__name__)

# Add custom Jinja2 filter for JSON serialization


@app.template_filter('tojsonfilter')
def tojson_filter(obj):
    return json.dumps(obj, ensure_ascii=False)


@app.route('/')
def home():
    return """
    <h1>🚀 AI Ultra Analysis System</h1>
    <p>Available interfaces:</p>
    <ul>
        <li><a href="/agent-ultra">Ultra Analysis Interface</a></li>
        <li><a href="/api/ultra-test">Test API</a></li>
    </ul>
    """


@app.route('/agent-ultra')
def agent_ultra_analysis():
    """Ultra Analysis interface"""
    # Demo customer data
    customer_ids = ['ultra_1001', 'ultra_1002', 'ultra_1003']
    customers_info = {
        'ultra_1001': {
            'display_name': 'Nguyễn Văn An - 28 tuổi (Healthy)',
            'age': 28,
            'preferences': ['healthy', 'vietnamese']
        },
        'ultra_1002': {
            'display_name': 'Trần Thị Bình - 35 tuổi (Quick meals)',
            'age': 35,
            'preferences': ['quick_meals', 'asian']
        },
        'ultra_1003': {
            'display_name': 'Lê Hoàng Cường - 42 tuổi (Hải sản)',
            'age': 42,
            'preferences': ['seafood', 'northern']
        }
    }

    return render_template('agent_ultra_analysis.html',
                           customer_ids=customer_ids,
                           customers_info=customers_info)


@app.route('/api/ultra-analysis', methods=['POST'])
def ultra_analysis_api():
    """Ultra Analysis API endpoint"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        customer_id = data.get('customer_id', '')
        step_id = data.get('step_id', '')

        if not message:
            return jsonify({
                'error': 'Message không được để trống',
                'status': 'error'
            }), 400

        # Process analysis
        processing_start = time.time()

        if step_id == 'ultra_input_analysis':
            result = process_input_analysis(message)
        elif step_id == 'ultra_customer_profiling':
            result = process_customer_profiling(customer_id, message)
        elif step_id == 'ultra_rag_search':
            result = process_rag_search(message)
        elif step_id == 'ultra_llm_processing':
            result = process_llm_processing(message, customer_id)
        elif step_id == 'ultra_response_optimization':
            result = process_response_optimization(message)
        else:
            # Full analysis
            result = process_full_analysis(message, customer_id)

        processing_time = (time.time() - processing_start) * 1000

        return jsonify({
            'status': 'success',
            'processing_time_ms': round(processing_time, 2),
            'step_id': step_id,
            'timestamp': time.time(),
            'result': result
        })

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


def process_input_analysis(message):
    """Phân tích đầu vào"""
    tokens = message.split()

    return {
        'tokens_count': len(tokens),
        'character_count': len(message),
        'intent_analysis': {
            'primary_intent': 'food_recommendation',
            'confidence': random.uniform(0.8, 0.95)
        },
        'entities_extracted': [
            {'type': 'FOOD_TYPE', 'value': 'healthy', 'confidence': 0.89}
        ],
        'sentiment_analysis': {
            'polarity': random.uniform(-0.1, 0.3),
            'emotion': 'curious'
        },
        'real_time_insights': [
            f"Processed {len(tokens)} tokens",
            f"Intent confidence: {random.uniform(0.8, 0.95):.2f}",
            "Entity extraction completed",
            "Sentiment analysis: positive"
        ]
    }


def process_customer_profiling(customer_id, message):
    """Phân tích profile khách hàng"""
    profiles = {
        'ultra_1001': {
            'demographics': {'age': 28, 'location': 'Hà Nội'},
            'preferences': ['healthy', 'vietnamese'],
            'behavior_cluster': 'health_conscious'
        },
        'ultra_1002': {
            'demographics': {'age': 35, 'location': 'TP.HCM'},
            'preferences': ['quick_meals', 'asian'],
            'behavior_cluster': 'busy_professional'
        }
    }

    profile = profiles.get(customer_id, {
        'demographics': {'age': 30, 'location': 'Unknown'},
        'preferences': ['general'],
        'behavior_cluster': 'general_user'
    })

    return {
        'customer_id': customer_id,
        'profile_data': profile,
        'profile_alignment': random.uniform(0.6, 0.9),
        'behavioral_insights': {
            'cluster': profile['behavior_cluster'],
            'satisfaction_prediction': random.uniform(0.7, 0.95)
        },
        'real_time_insights': [
            f"Profile loaded for {customer_id}",
            f"Behavior cluster: {profile['behavior_cluster']}",
            f"Alignment score: {random.uniform(0.6, 0.9):.2f}",
            "Personalization applied"
        ]
    }


def process_rag_search(message):
    """Tìm kiếm RAG"""
    mock_documents = [
        {'id': 'doc_001', 'title': 'Healthy Vietnamese Recipes', 'similarity': 0.92},
        {'id': 'doc_002', 'title': 'Asian Cuisine Guide', 'similarity': 0.89},
        {'id': 'doc_003', 'title': 'Budget Meal Plans', 'similarity': 0.86}
    ]

    return {
        'query_processing': {
            'original_query': message,
            'embedding_dimensions': 768
        },
        'search_results': {
            'total_documents_searched': 1247,
            'retrieved_documents': len(mock_documents)
        },
        'similarity_analysis': {
            'highest_similarity': max(doc['similarity'] for doc in mock_documents),
            'average_similarity': sum(doc['similarity'] for doc in mock_documents) / len(mock_documents)
        },
        'retrieved_documents': mock_documents,
        'real_time_insights': [
            f"Searched {1247} documents",
            f"Retrieved {len(mock_documents)} relevant docs",
            f"Highest similarity: {max(doc['similarity'] for doc in mock_documents):.3f}",
            "Context prepared for LLM"
        ]
    }


def process_llm_processing(message, customer_id):
    """Xử lý LLM"""
    prompt_tokens = len(message.split()) * 1.3
    completion_tokens = random.randint(100, 300)

    return {
        'model_info': {
            'model_name': 'gpt-4-turbo',
            'context_window': 128000
        },
        'token_usage': {
            'prompt_tokens': int(prompt_tokens),
            'completion_tokens': completion_tokens,
            'total_tokens': int(prompt_tokens + completion_tokens)
        },
        'generation_parameters': {
            'temperature': 0.7,
            'top_p': 0.9
        },
        'quality_metrics': {
            'response_relevance': random.uniform(0.85, 0.98),
            'factual_accuracy': random.uniform(0.90, 0.99)
        },
        'real_time_insights': [
            f"Generated {completion_tokens} tokens",
            f"Processing time: ~{random.randint(800, 2000)}ms",
            f"Quality score: {random.uniform(0.85, 0.98):.3f}",
            "Response generation completed"
        ]
    }


def process_response_optimization(message):
    """Tối ưu hóa response"""
    return {
        'optimization_stages': {
            'content_validation': {'passed': True},
            'fact_checking': {'accuracy_score': random.uniform(0.92, 0.99)},
            'personalization': {'level': 'high', 'adjustments': 5}
        },
        'quality_assurance': {
            'readability_score': random.uniform(0.80, 0.95),
            'tone_consistency': random.uniform(0.88, 0.96)
        },
        'final_validation': {
            'overall_quality_score': random.uniform(0.90, 0.98),
            'user_satisfaction_prediction': random.uniform(0.85, 0.95)
        },
        'real_time_insights': [
            "Content validation passed",
            f"Quality score: {random.uniform(0.90, 0.98):.3f}",
            "Personalization applied",
            "Optimization completed"
        ]
    }


def process_full_analysis(message, customer_id):
    """Full analysis pipeline"""
    pipeline_start = time.time()

    steps_results = {
        'ultra_input_analysis': process_input_analysis(message),
        'ultra_customer_profiling': process_customer_profiling(customer_id, message),
        'ultra_rag_search': process_rag_search(message),
        'ultra_llm_processing': process_llm_processing(message, customer_id),
        'ultra_response_optimization': process_response_optimization(message)
    }

    pipeline_time = (time.time() - pipeline_start) * 1000

    ai_response = f"""
    🎯 **Phân tích hoàn tất cho: "{message}"**
    
    **📊 Kết quả tổng hợp:**
    - 🧠 Input Analysis: Xác định intent với độ tin cậy cao
    - 👤 Customer Profile: Khớp profile {random.uniform(0.7, 0.9):.1%}
    - 🔍 RAG Search: Tìm thấy {random.randint(5, 10)} documents liên quan
    - 🤖 LLM Processing: Generate response chất lượng cao
    - ✨ Optimization: Đạt quality score {random.uniform(0.9, 0.98):.2f}
    
    **🎯 Recommendations:**
    - Món ăn healthy phù hợp với profile khách hàng
    - Cân bằng dinh dưỡng và ngân sách
    - Tích hợp sở thích cá nhân
    """

    return {
        'pipeline_summary': {
            'total_processing_time_ms': round(pipeline_time, 2),
            'steps_completed': len(steps_results),
            'overall_success_rate': 1.0,
            'confidence_score': random.uniform(0.88, 0.97)
        },
        'steps_results': steps_results,
        'ai_response': ai_response,        'performance_metrics': {
            'throughput': f"{len(message.split())/max(pipeline_time, 0.001)*1000:.2f} tokens/sec",
            'accuracy_aggregate': random.uniform(0.92, 0.98),
            'system_efficiency': random.uniform(0.85, 0.95)
        }
    }


@app.route('/api/ultra-test')
def test_api():
    """Test API endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Ultra Analysis API is working!',
        'timestamp': time.time()
    })


if __name__ == '__main__':
    print("🚀 Starting Ultra Analysis System...")
    print("=" * 50)
    print("🌐 Ultra Analysis: http://127.0.0.1:5001/agent-ultra")
    print("🔧 Test API: http://127.0.0.1:5001/api/ultra-test")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5001)
