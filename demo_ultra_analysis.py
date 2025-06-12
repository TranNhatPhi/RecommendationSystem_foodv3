#!/usr/bin/env python3
"""
🚀 Ultra Analysis System - Interactive Demo
Comprehensive showcase of ultra-detailed AI analysis capabilities
"""

import requests
import json
import time
import sys
from datetime import datetime

# Demo configuration
ULTRA_API_URL = "http://127.0.0.1:5001/api/ultra-analysis"
INTERFACE_URL = "http://127.0.0.1:5001/agent-ultra"

# Demo queries with different complexity levels
DEMO_QUERIES = [
    {
        "level": "🌟 BASIC",
        "query": "Gợi ý món healthy cho bữa trưa",
        "customer": "ultra_1001",
        "description": "Simple food recommendation với basic analysis"
    },
    {
        "level": "🔥 INTERMEDIATE",
        "query": "Phân tích thực đơn giảm cân 7 ngày cho người tiểu đường với ngân sách 200k",
        "customer": "ultra_1002",
        "description": "Complex diet planning với multiple constraints"
    },
    {
        "level": "💎 ADVANCED",
        "query": "Thiết kế menu fusion Việt-Âu cho event cao cấp 50 khách, cân bằng dinh dưỡng và thẩm mỹ, phù hợp văn hóa đa quốc gia",
        "customer": "ultra_1003",
        "description": "Enterprise-level menu design với cultural considerations"
    }
]


def print_header():
    """Print demo header"""
    print("🚀" + "=" * 80 + "🚀")
    print("🌟" + " " * 28 + "ULTRA ANALYSIS DEMO" + " " * 28 + "🌟")
    print("🚀" + "=" * 80 + "🚀")
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Interface URL: {INTERFACE_URL}")
    print(f"🔧 API Endpoint: {ULTRA_API_URL}")
    print("🚀" + "=" * 80 + "🚀")


def check_system_status():
    """Check if Ultra Analysis system is running"""
    print("\n🔍 Checking Ultra Analysis System Status...")

    try:
        # Check interface
        interface_response = requests.get("http://127.0.0.1:5001/", timeout=5)
        interface_status = "✅ ONLINE" if interface_response.status_code == 200 else "❌ OFFLINE"

        # Check API
        api_response = requests.get(
            "http://127.0.0.1:5001/api/ultra-test", timeout=5)
        api_status = "✅ ONLINE" if api_response.status_code == 200 else "❌ OFFLINE"

        print(f"🌐 Interface: {interface_status}")
        print(f"🔧 API: {api_status}")

        if interface_response.status_code == 200 and api_response.status_code == 200:
            print("✅ System is fully operational!")
            return True
        else:
            print("❌ System is not fully operational!")
            return False

    except Exception as e:
        print(f"❌ System check failed: {e}")
        print("💡 Make sure to run: python ultra_analysis_app.py")
        return False


def demo_individual_step(step_id, query, customer_id):
    """Demo individual processing step"""
    print(f"\n🔬 Testing Step: {step_id}")

    try:
        data = {
            "message": query,
            "customer_id": customer_id,
            "step_id": step_id
        }

        start_time = time.time()
        response = requests.post(ULTRA_API_URL, json=data, timeout=10)
        processing_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success - {processing_time:.1f}ms")

            # Show key insights
            if 'result' in result and 'real_time_insights' in result['result']:
                # Show first 2 insights
                insights = result['result']['real_time_insights'][:2]
                for insight in insights:
                    print(f"   💡 {insight}")

            return True
        else:
            print(f"   ❌ Failed - {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Error - {e}")
        return False


def demo_full_analysis(query_data):
    """Demo full ultra analysis pipeline"""
    print(f"\n🎯 {query_data['level']} ANALYSIS")
    print("─" * 60)
    print(f"📝 Query: {query_data['query']}")
    print(f"👤 Customer: {query_data['customer']}")
    print(f"📋 Description: {query_data['description']}")
    print("─" * 60)

    try:
        data = {
            "message": query_data['query'],
            "customer_id": query_data['customer'],
            "step_id": ""  # Full analysis
        }

        print("🚀 Starting full ultra analysis...")
        start_time = time.time()

        response = requests.post(ULTRA_API_URL, json=data, timeout=30)
        total_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            result = response.json()

            print(f"✅ Analysis Complete - {total_time:.1f}ms")
            print("\n📊 RESULTS SUMMARY:")

            # Show pipeline summary
            if 'result' in result and 'pipeline_summary' in result['result']:
                pipeline = result['result']['pipeline_summary']
                print(
                    f"   ⏱️ Processing Time: {pipeline.get('total_processing_time_ms', 0):.1f}ms")
                print(
                    f"   📈 Steps Completed: {pipeline.get('steps_completed', 0)}/5")
                print(
                    f"   🎯 Success Rate: {pipeline.get('overall_success_rate', 0)*100:.0f}%")
                print(
                    f"   🔥 Confidence: {pipeline.get('confidence_score', 0):.2f}")

            # Show AI response preview
            if 'result' in result and 'ai_response' in result['result']:
                ai_response = result['result']['ai_response'][:200] + "..." if len(
                    result['result']['ai_response']) > 200 else result['result']['ai_response']
                print(f"\n🤖 AI Response Preview:")
                print(f"   {ai_response}")

            # Show performance metrics
            if 'result' in result and 'performance_metrics' in result['result']:
                metrics = result['result']['performance_metrics']
                print(f"\n⚡ Performance Metrics:")
                for key, value in metrics.items():
                    print(f"   📊 {key}: {value}")

            return True
        else:
            print(f"❌ Analysis Failed - {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Analysis Error - {e}")
        return False


def demo_step_by_step_analysis():
    """Demo individual step analysis"""
    print("\n🔬 STEP-BY-STEP ANALYSIS DEMO")
    print("=" * 60)

    steps = [
        'ultra_input_analysis',
        'ultra_customer_profiling',
        'ultra_rag_search',
        'ultra_llm_processing',
        'ultra_response_optimization'
    ]

    test_query = "Phân tích món healthy protein cao"
    test_customer = "ultra_1001"

    print(f"📝 Test Query: {test_query}")
    print(f"👤 Test Customer: {test_customer}")

    successful_steps = 0
    for step in steps:
        if demo_individual_step(step, test_query, test_customer):
            successful_steps += 1
        time.sleep(0.5)  # Small delay between steps

    print(
        f"\n📊 Step Analysis Summary: {successful_steps}/{len(steps)} successful")
    return successful_steps == len(steps)


def demo_performance_test():
    """Demo performance and load testing"""
    print("\n⚡ PERFORMANCE TESTING DEMO")
    print("=" * 60)

    test_queries = [
        {"message": "Quick healthy meal", "customer_id": "ultra_1001"},
        {"message": "Budget family dinner", "customer_id": "ultra_1002"},
        {"message": "Protein rich breakfast", "customer_id": "ultra_1003"}
    ]

    print("🚀 Running concurrent performance test...")

    try:
        import concurrent.futures

        def single_request(query_data):
            start_time = time.time()
            response = requests.post(
                ULTRA_API_URL, json=query_data, timeout=15)
            processing_time = (time.time() - start_time) * 1000

            return {
                'success': response.status_code == 200,
                'time': processing_time,
                'query': query_data['message']
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(single_request, query)
                       for query in test_queries]
            results = [future.result() for future in concurrent.futures.as_completed(
                futures, timeout=30)]

        successful_requests = sum(1 for r in results if r['success'])
        avg_time = sum(r['time'] for r in results if r['success']
                       ) / max(successful_requests, 1)

        print(f"✅ Performance Test Results:")
        print(
            f"   📊 Successful Requests: {successful_requests}/{len(test_queries)}")
        print(f"   ⏱️ Average Response Time: {avg_time:.1f}ms")
        print(
            f"   🚀 Concurrent Processing: {'✅ Passed' if successful_requests == len(test_queries) else '⚠️ Issues'}")

        for result in results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['query']}: {result['time']:.1f}ms")

        return successful_requests == len(test_queries)

    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False


def interactive_demo():
    """Interactive demo mode"""
    print("\n🎮 INTERACTIVE DEMO MODE")
    print("=" * 60)
    print("Enter your own queries to test Ultra Analysis!")
    print("Type 'quit' to exit, 'help' for commands")

    while True:
        try:
            print("\n💬 Enter your query (or command):")
            user_input = input("🎯 > ").strip()

            if user_input.lower() == 'quit':
                print("👋 Thanks for trying Ultra Analysis!")
                break
            elif user_input.lower() == 'help':
                print("📚 Available commands:")
                print("   • Any food-related query for analysis")
                print("   • 'quit' - Exit interactive mode")
                print("   • 'help' - Show this help")
                continue
            elif not user_input:
                print("⚠️ Please enter a query!")
                continue

            # Run analysis
            data = {
                "message": user_input,
                "customer_id": "ultra_1001",
                "step_id": ""
            }

            print("🚀 Analyzing your query...")
            start_time = time.time()

            response = requests.post(ULTRA_API_URL, json=data, timeout=20)
            processing_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis Complete - {processing_time:.1f}ms")

                if 'result' in result and 'ai_response' in result['result']:
                    print("\n🤖 AI Response:")
                    print(result['result']['ai_response'])
                else:
                    print("📊 Analysis completed successfully!")
            else:
                print(f"❌ Analysis failed: {response.status_code}")

        except KeyboardInterrupt:
            print("\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main demo function"""
    print_header()

    # Check system status
    if not check_system_status():
        print("\n💡 Please start Ultra Analysis system first:")
        print("   python ultra_analysis_app.py")
        return

    print("\n🎯 DEMO MENU:")
    print("1. 🔥 Full Analysis Demo (Recommended)")
    print("2. 🔬 Step-by-Step Analysis")
    print("3. ⚡ Performance Testing")
    print("4. 🎮 Interactive Mode")
    print("5. 🚀 Complete Showcase (All demos)")

    try:
        choice = input("\n🎯 Select demo option (1-5): ").strip()

        if choice == "1":
            print("\n🔥 RUNNING FULL ANALYSIS DEMO")
            print("=" * 60)
            success_count = 0
            for query_data in DEMO_QUERIES:
                if demo_full_analysis(query_data):
                    success_count += 1
                print()

            print(
                f"🎯 Full Analysis Demo Summary: {success_count}/{len(DEMO_QUERIES)} successful")

        elif choice == "2":
            demo_step_by_step_analysis()

        elif choice == "3":
            demo_performance_test()

        elif choice == "4":
            interactive_demo()

        elif choice == "5":
            print("\n🚀 COMPLETE ULTRA ANALYSIS SHOWCASE")
            print("=" * 80)

            # Run all demos
            print("\n1️⃣ Full Analysis Demo...")
            success_count = 0
            for query_data in DEMO_QUERIES:
                if demo_full_analysis(query_data):
                    success_count += 1

            print("\n2️⃣ Step-by-Step Analysis...")
            step_success = demo_step_by_step_analysis()

            print("\n3️⃣ Performance Testing...")
            perf_success = demo_performance_test()

            # Summary
            print("\n🎯 COMPLETE SHOWCASE SUMMARY")
            print("=" * 60)
            print(
                f"🔥 Full Analysis: {success_count}/{len(DEMO_QUERIES)} successful")
            print(
                f"🔬 Step Analysis: {'✅ Passed' if step_success else '❌ Failed'}")
            print(
                f"⚡ Performance: {'✅ Passed' if perf_success else '❌ Failed'}")

            if success_count == len(DEMO_QUERIES) and step_success and perf_success:
                print("\n🎉 ALL DEMOS PASSED! Ultra Analysis system is fully functional!")
            else:
                print("\n⚠️ Some demos had issues, check system configuration")

        else:
            print("⚠️ Invalid option selected")

    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")

    print("\n🌟 Demo completed!")
    print(f"🌐 Access Ultra Analysis Interface: {INTERFACE_URL}")
    print("📚 See ULTRA_ANALYSIS_COMPLETION.md for full documentation")


if __name__ == "__main__":
    main()
