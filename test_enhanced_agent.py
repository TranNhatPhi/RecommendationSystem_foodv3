"""
Enhanced Testing Script for AI Agent System
Tests all features including performance monitoring and caching
"""

import requests
import json
import time
import asyncio
import concurrent.futures
from typing import Dict, List
import random


class EnhancedAgentTester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def test_basic_functionality(self):
        """Test basic AI agent functionality"""
        print("🧪 Testing Basic AI Agent Functionality...")

        test_cases = [
            {
                "name": "Health inquiry",
                "message": "Tôi muốn ăn món gì tốt cho sức khỏe?",
                "user_id": "CUS00001",
                "location": "Hà Nội"
            },
            {
                "name": "Diabetes consultation",
                "message": "Tôi bị tiểu đường, gợi ý món ăn phù hợp",
                "user_id": "CUS00002",
                "location": "TP.HCM"
            },
            {
                "name": "Weight loss advice",
                "message": "Món ăn nào phù hợp cho người giảm cân?",
                "user_id": "CUS00003",
                "location": "Đà Nẵng"
            },
            {
                "name": "Vietnamese cuisine",
                "message": "Tôi thích món ăn Việt Nam, bạn gợi ý giúp thực đơn an toàn",
                "user_id": "CUS00004",
                "location": "Cần Thơ"
            }
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"  Test {i}/{len(test_cases)}: {test_case['name']}")

            start_time = time.time()

            try:
                response = self.session.post(
                    f"{self.base_url}/api/agent_chat",
                    json=test_case,
                    timeout=30
                )

                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"    ✅ Passed ({duration:.2f}s)")
                        self.test_results.append({
                            "test": test_case['name'],
                            "status": "PASS",
                            "duration": duration,
                            "response_length": len(data.get('ai_response', '')),
                            "recipes_count": len(data.get('recommended_recipes', [])),
                            "restaurants_count": len(data.get('nearby_restaurants', []))
                        })
                    else:
                        print(
                            f"    ❌ Failed: {data.get('error', 'Unknown error')}")
                        self.test_results.append({
                            "test": test_case['name'],
                            "status": "FAIL",
                            "error": data.get('error', 'Unknown error')
                        })
                else:
                    print(f"    ❌ HTTP Error: {response.status_code}")
                    self.test_results.append({
                        "test": test_case['name'],
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    })

            except Exception as e:
                print(f"    ❌ Exception: {str(e)}")
                self.test_results.append({
                    "test": test_case['name'],
                    "status": "ERROR",
                    "error": str(e)
                })

            time.sleep(1)  # Rate limiting

    def test_performance_endpoints(self):
        """Test performance monitoring endpoints"""
        print("\n📊 Testing Performance Monitoring...")

        endpoints = [
            ("/api/agent_stats", "Agent Statistics"),
            ("/api/performance/health", "Health Check"),
            ("/api/performance/metrics", "Performance Metrics"),
            ("/api/cache/stats", "Cache Statistics"),
            ("/api/system/info", "System Information")
        ]

        for endpoint, name in endpoints:
            print(f"  Testing {name}...")

            try:
                start_time = time.time()
                response = self.session.get(
                    f"{self.base_url}{endpoint}", timeout=10)
                duration = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    print(f"    ✅ Passed ({duration:.2f}s)")

                    # Log some key metrics
                    if endpoint == "/api/agent_stats" and 'stats' in data:
                        stats = data['stats']
                        print(
                            f"      📊 Recipes: {stats.get('recipes_count', 'N/A')}")
                        print(
                            f"      👥 Customers: {stats.get('customers_count', 'N/A')}")
                        print(
                            f"      🎯 Accuracy: {stats.get('ai_accuracy', 'N/A')}%")

                    elif endpoint == "/api/performance/health":
                        print(
                            f"      🏥 Status: {data.get('status', 'Unknown')}")
                        components = data.get('components', {})
                        for comp, status in components.items():
                            print(f"      ↳ {comp}: {status}")

                    elif endpoint == "/api/system/info" and 'system_info' in data:
                        features = data['system_info'].get('features', {})
                        enabled_features = [
                            k for k, v in features.items() if v]
                        print(
                            f"      🎛️ Features: {', '.join(enabled_features)}")

                elif response.status_code == 503:
                    print(f"    ⚠️ Service Unavailable (expected for some endpoints)")
                else:
                    print(f"    ❌ HTTP Error: {response.status_code}")

            except Exception as e:
                print(f"    ❌ Exception: {str(e)}")

    def test_semantic_search(self):
        """Test semantic search functionality"""
        print("\n🔍 Testing Semantic Search...")

        search_queries = [
            "món ăn Việt Nam healthy",
            "salad giảm cân",
            "món ăn cho người tiểu đường",
            "thức ăn nhanh dinh dưỡng",
            "món chay healthy"
        ]

        for query in search_queries:
            print(f"  Searching: '{query}'")

            try:
                response = self.session.post(
                    f"{self.base_url}/api/semantic_search",
                    json={
                        "query": query,
                        "n_results": 5
                    },
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        results_count = len(data.get('results', []))
                        print(f"    ✅ Found {results_count} results")
                    else:
                        print(f"    ❌ Search failed: {data.get('error')}")
                else:
                    print(f"    ❌ HTTP Error: {response.status_code}")

            except Exception as e:
                print(f"    ❌ Exception: {str(e)}")

            time.sleep(0.5)

    def test_load_performance(self, concurrent_requests: int = 5, total_requests: int = 20):
        """Test system performance under load"""
        print(
            f"\n⚡ Testing Load Performance ({concurrent_requests} concurrent, {total_requests} total)...")

        def make_request(request_id):
            messages = [
                "Tôi muốn ăn gì hôm nay?",
                "Món ăn nào tốt cho sức khỏe?",
                "Gợi ý món ăn Việt Nam",
                "Thực đơn cho người giảm cân",
                "Món ăn dinh dưỡng cho trẻ em"
            ]

            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/agent_chat",
                    json={
                        "message": random.choice(messages),
                        "user_id": f"TEST{request_id:03d}",
                        "location": "Test Location"
                    },
                    timeout=30
                )
                duration = time.time() - start_time

                return {
                    "request_id": request_id,
                    "success": response.status_code == 200,
                    "duration": duration,
                    "status_code": response.status_code
                }

            except Exception as e:
                return {
                    "request_id": request_id,
                    "success": False,
                    "duration": 0,
                    "error": str(e)
                }

        # Execute concurrent requests
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(make_request, i)
                       for i in range(total_requests)]
            results = [future.result()
                       for future in concurrent.futures.as_completed(futures)]

        total_duration = time.time() - start_time

        # Analyze results
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]

        if successful_requests:
            avg_response_time = sum(
                r['duration'] for r in successful_requests) / len(successful_requests)
            max_response_time = max(r['duration'] for r in successful_requests)
            min_response_time = min(r['duration'] for r in successful_requests)
        else:
            avg_response_time = max_response_time = min_response_time = 0

        print(f"  📊 Results:")
        print(f"    Total time: {total_duration:.2f}s")
        print(f"    Successful: {len(successful_requests)}/{total_requests}")
        print(f"    Failed: {len(failed_requests)}")
        print(
            f"    Success rate: {len(successful_requests)/total_requests*100:.1f}%")
        print(f"    Avg response time: {avg_response_time:.2f}s")
        print(f"    Min response time: {min_response_time:.2f}s")
        print(f"    Max response time: {max_response_time:.2f}s")
        print(f"    Requests/second: {total_requests/total_duration:.2f}")

        if failed_requests:
            print(f"  ❌ Failures:")
            for failure in failed_requests[:5]:  # Show first 5 failures
                error = failure.get(
                    'error', f"HTTP {failure.get('status_code')}")
                print(f"    Request {failure['request_id']}: {error}")

    def generate_report(self):
        """Generate test report"""
        print("\n📋 Test Report Summary:")
        print("=" * 50)

        passed_tests = len(
            [r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len(
            [r for r in self.test_results if r['status'] in ['FAIL', 'ERROR']])
        total_tests = len(self.test_results)

        if total_tests > 0:
            success_rate = passed_tests / total_tests * 100
            print(f"Total Tests: {total_tests}")
            print(f"Passed: {passed_tests}")
            print(f"Failed: {failed_tests}")
            print(f"Success Rate: {success_rate:.1f}%")

            if passed_tests > 0:
                avg_duration = sum(r.get(
                    'duration', 0) for r in self.test_results if r['status'] == 'PASS') / passed_tests
                print(f"Average Response Time: {avg_duration:.2f}s")

        print("\n🏆 System Status: " +
              ("✅ HEALTHY" if failed_tests == 0 else "⚠️ NEEDS ATTENTION"))


def main():
    print("🚀 Enhanced AI Agent System Testing")
    print("=" * 50)

    tester = EnhancedAgentTester()

    # Run all tests
    tester.test_basic_functionality()
    tester.test_performance_endpoints()
    tester.test_semantic_search()
    tester.test_load_performance()

    # Generate report
    tester.generate_report()

    print("\n✨ Testing completed!")


if __name__ == "__main__":
    main()
