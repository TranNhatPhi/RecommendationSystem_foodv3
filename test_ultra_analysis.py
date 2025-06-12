#!/usr/bin/env python3
"""
Test script for Ultra Analysis interface
Tests both frontend functionality and API endpoints
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://127.0.0.1:5001"  # Ultra Analysis runs on port 5001
TEST_MESSAGES = [
    "Phân tích món healthy có protein cao cho gia đình 4 người",
    "Gợi ý thực đơn giảm cân khoa học với budget 200k",
    "Tư vấn món Việt Nam truyền thống cho bữa tối",
    "Menu fusion Âu-Á cho event cao cấp 20 khách"
]

TEST_CUSTOMERS = [
    "ultra_1001",
    "ultra_1002",
    "ultra_1003",
    "ultra_1004"
]


def test_ultra_interface():
    """Test Ultra Analysis interface accessibility"""
    print("🔍 Testing Ultra Analysis Interface...")

    try:
        response = requests.get(f"{BASE_URL}/agent-ultra")
        if response.status_code == 200:
            print("✅ Ultra Analysis interface accessible")

            # Check for key elements in HTML
            html_content = response.text
            required_elements = [
                "AI Agent Ultra Analysis",
                "Ultra Deep Analysis Dashboard",
                "agent_ultra_analysis.html",
                "sendUltraMessage",
                "processUltraAnalysisWithAPI"
            ]

            missing_elements = []
            for element in required_elements:
                if element not in html_content:
                    missing_elements.append(element)

            if missing_elements:
                print(f"⚠️ Missing elements: {missing_elements}")
            else:
                print("✅ All key interface elements present")

            return True
        else:
            print(f"❌ Interface not accessible: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Interface test failed: {e}")
        return False


def test_ultra_api_endpoint():
    """Test Ultra Analysis API endpoint"""
    print("\n🔧 Testing Ultra Analysis API...")

    try:
        # Test full ultra analysis
        test_data = {
            "message": TEST_MESSAGES[0],
            "customer_id": TEST_CUSTOMERS[0],
            "step_id": ""  # Full analysis
        }

        response = requests.post(
            f"{BASE_URL}/api/ultra-analysis",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Full ultra analysis API working")

            # Validate response structure
            required_fields = ['status', 'processing_time_ms', 'result']
            missing_fields = [
                field for field in required_fields if field not in result]

            if missing_fields:
                print(f"⚠️ Missing API fields: {missing_fields}")
            else:
                print(
                    f"✅ API response complete - Processing time: {result['processing_time_ms']:.2f}ms")

            # Test individual steps
            test_individual_steps()

            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ API test error: {e}")
        return False


def test_individual_steps():
    """Test individual ultra analysis steps"""
    print("\n🔬 Testing Individual Steps...")

    steps = [
        'ultra_input_analysis',
        'ultra_customer_profiling',
        'ultra_rag_search',
        'ultra_llm_processing',
        'ultra_response_optimization'
    ]

    results = {}

    for step in steps:
        try:
            test_data = {
                "message": TEST_MESSAGES[1],
                "customer_id": TEST_CUSTOMERS[1],
                "step_id": step
            }

            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/ultra-analysis",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            processing_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                results[step] = {
                    'status': 'success',
                    'processing_time': processing_time,
                    'api_time': result.get('processing_time_ms', 0)
                }
                print(f"✅ {step}: {processing_time:.1f}ms")
            else:
                results[step] = {'status': 'failed',
                                 'error': response.status_code}
                print(f"❌ {step}: Failed ({response.status_code})")

        except Exception as e:
            results[step] = {'status': 'error', 'error': str(e)}
            print(f"❌ {step}: Error - {e}")

    # Summary
    successful_steps = sum(1 for r in results.values()
                           if r['status'] == 'success')
    print(f"\n📊 Step Test Summary: {successful_steps}/{len(steps)} successful")

    return results


def test_performance_metrics():
    """Test performance under load"""
    print("\n⚡ Testing Performance Metrics...")

    try:
        # Test multiple concurrent requests
        import concurrent.futures
        import threading

        def single_request(message_idx):
            test_data = {
                "message": TEST_MESSAGES[message_idx % len(TEST_MESSAGES)],
                "customer_id": TEST_CUSTOMERS[message_idx % len(TEST_CUSTOMERS)],
                "step_id": ""
            }

            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/ultra-analysis",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            processing_time = (time.time() - start_time) * 1000

            return {
                'status_code': response.status_code,
                'processing_time': processing_time,
                'success': response.status_code == 200
            }

        # Run 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(single_request, i) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(
                futures, timeout=60)]

        successful_requests = sum(1 for r in results if r['success'])
        avg_processing_time = sum(
            r['processing_time'] for r in results if r['success']) / max(successful_requests, 1)

        print(f"✅ Performance Test Complete:")
        print(f"   - Successful requests: {successful_requests}/5")
        print(f"   - Average processing time: {avg_processing_time:.1f}ms")
        print(
            f"   - Concurrent processing: {'✅ Passed' if successful_requests >= 4 else '⚠️ Issues detected'}")

        return successful_requests >= 4

    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False


def test_data_quality():
    """Test quality of ultra analysis data"""
    print("\n🎯 Testing Data Quality...")

    try:
        test_data = {
            "message": "Phân tích chi tiết món healthy protein cao ngân sách 300k cho người tiểu đường",
            "customer_id": "ultra_1001",
            "step_id": ""
        }

        response = requests.post(
            f"{BASE_URL}/api/ultra-analysis",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            analysis = result.get('result', {})

            quality_checks = {
                'steps_results_present': 'steps_results' in analysis,
                'ai_response_generated': 'ai_response' in analysis and len(analysis.get('ai_response', '')) > 10,
                'pipeline_metrics': 'pipeline_summary' in analysis,
                'performance_data': 'performance_metrics' in analysis
            }

            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)

            print(
                f"✅ Data Quality: {passed_checks}/{total_checks} checks passed")

            for check, passed in quality_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")

            # Check individual step data quality
            if 'steps_results' in analysis:
                step_quality = {}
                for step_name, step_data in analysis['steps_results'].items():
                    has_insights = 'real_time_insights' in step_data
                    has_metrics = any(key.endswith('_analysis') or key.endswith(
                        '_metrics') for key in step_data.keys())
                    step_quality[step_name] = has_insights and has_metrics

                quality_steps = sum(step_quality.values())
                print(
                    f"✅ Step Data Quality: {quality_steps}/{len(step_quality)} steps have complete data")

            return passed_checks >= 3
        else:
            print(f"❌ Data quality test failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Data quality test error: {e}")
        return False


def main():
    """Run comprehensive Ultra Analysis tests"""
    print("🚀 Starting Ultra Analysis Comprehensive Test Suite")
    print("=" * 60)

    test_results = {
        'interface': test_ultra_interface(),
        'api': test_ultra_api_endpoint(),
        'performance': test_performance_metrics(),
        'data_quality': test_data_quality()
    }

    print("\n" + "=" * 60)
    print("📋 ULTRA ANALYSIS TEST SUMMARY")
    print("=" * 60)

    total_tests = len(test_results)
    passed_tests = sum(test_results.values())

    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.upper():.<20} {status}")

    print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Ultra Analysis system is fully functional!")
        return 0
    elif passed_tests >= total_tests * 0.75:
        print("⚠️ Most tests passed, system is mostly functional with minor issues")
        return 1
    else:
        print("❌ Multiple test failures detected, system needs attention")
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
