#!/usr/bin/env python3
"""
Simple test to check agent template rendering
"""

from flask import Flask, render_template
import json

app = Flask(__name__)


@app.template_filter('tojsonfilter')
def tojson_filter(obj):
    return json.dumps(obj, ensure_ascii=False)


@app.route('/test-agent')
def test_agent():
    """Test agent template with simple data"""
    try:
        # Simple test data
        customer_ids = ['CUS001', 'CUS002', 'CUS003']
        customers_info = {
            'CUS001': {'name': 'Test Customer 1', 'age': 25},
            'CUS002': {'name': 'Test Customer 2', 'age': 30},
            'CUS003': {'name': 'Test Customer 3', 'age': 35}
        }

        print(f"✅ Rendering with {len(customer_ids)} customers")
        return render_template('agent.html',
                               customer_ids=customer_ids,
                               customers_info=customers_info)
    except Exception as e:
        print(f"❌ Template error: {e}")
        import traceback
        traceback.print_exc()
        return f"<h1>Template Error</h1><pre>{str(e)}</pre><pre>{traceback.format_exc()}</pre>"


@app.route('/simple')
def simple_test():
    """Super simple test"""
    return "<h1>✅ Flask is working!</h1><p>If you see this, the basic Flask setup is fine.</p>"


if __name__ == '__main__':
    print("🧪 Testing agent template...")
    print("URLs:")
    print("- Simple test: http://127.0.0.1:5001/simple")
    print("- Agent template test: http://127.0.0.1:5001/test-agent")
    app.run(debug=True, port=5001)
