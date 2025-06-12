#!/usr/bin/env python3
"""
Debug script to isolate template rendering issues
"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/test')
def test_template():
    """Simple test to check if template renders"""
    try:
        # Test with simple data
        customer_ids = ['CUS001', 'CUS002', 'CUS003']
        customers_info = {
            'CUS001': {'name': 'Test Customer 1', 'age': 25},
            'CUS002': {'name': 'Test Customer 2', 'age': 30},
            'CUS003': {'name': 'Test Customer 3', 'age': 35}
        }

        print(f"Rendering with customer_ids: {customer_ids}")
        print(f"Rendering with customers_info: {customers_info}")

        return render_template('agent.html',
                               customer_ids=customer_ids,
                               customers_info=customers_info)
    except Exception as e:
        print(f"Template error: {e}")
        import traceback
        traceback.print_exc()
        return f"<h1>Template Error</h1><pre>{str(e)}</pre><pre>{traceback.format_exc()}</pre>"


@app.route('/simple')
def simple_test():
    """Even simpler test"""
    return "<h1>Simple Test Works!</h1><p>If you see this, Flask is working.</p>"


if __name__ == '__main__':
    print("🧪 Starting debug template test...")
    print("Test URLs:")
    print("- Simple test: http://127.0.0.1:5001/simple")
    print("- Template test: http://127.0.0.1:5001/test")
    app.run(debug=True, port=5001)
