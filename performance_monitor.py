"""
Performance Monitor for AI Agent System
Tracks system performance metrics and provides analytics
"""

import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
from collections import defaultdict, deque


class PerformanceMonitor:
    def __init__(self, max_history: int = 1000):
        """Initialize performance monitor"""
        self.max_history = max_history
        self.request_times = deque(maxlen=max_history)
        self.api_calls = defaultdict(list)
        self.error_count = defaultdict(int)
        self.cache_stats = {'hits': 0, 'misses': 0}
        self.start_time = time.time()
        self._lock = threading.Lock()

        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)

    def log_request(self, endpoint: str, duration: float, success: bool = True):
        """Log a request with timing information"""
        with self._lock:
            timestamp = time.time()

            self.request_times.append({
                'timestamp': timestamp,
                'endpoint': endpoint,
                'duration': duration,
                'success': success
            })

            self.api_calls[endpoint].append({
                'timestamp': timestamp,
                'duration': duration,
                'success': success
            })

            if not success:
                self.error_count[endpoint] += 1

    def log_cache_hit(self):
        """Log cache hit"""
        with self._lock:
            self.cache_stats['hits'] += 1

    def log_cache_miss(self):
        """Log cache miss"""
        with self._lock:
            self.cache_stats['misses'] += 1

    def get_performance_stats(self) -> Dict:
        """Get current performance statistics"""
        with self._lock:
            now = time.time()
            uptime = now - self.start_time

            # Calculate averages for last hour
            hour_ago = now - 3600
            recent_requests = [
                r for r in self.request_times if r['timestamp'] > hour_ago]

            if recent_requests:
                avg_response_time = sum(
                    r['duration'] for r in recent_requests) / len(recent_requests)
                success_rate = sum(
                    1 for r in recent_requests if r['success']) / len(recent_requests) * 100
                requests_per_hour = len(recent_requests)
            else:
                avg_response_time = 0
                success_rate = 100
                requests_per_hour = 0

            # Cache performance
            total_cache_requests = self.cache_stats['hits'] + \
                self.cache_stats['misses']
            cache_hit_rate = (
                self.cache_stats['hits'] / total_cache_requests * 100) if total_cache_requests > 0 else 0

            return {
                'uptime_hours': uptime / 3600,
                'total_requests': len(self.request_times),
                'requests_per_hour': requests_per_hour,
                'avg_response_time_ms': avg_response_time * 1000,
                'success_rate_percent': success_rate,
                'cache_hit_rate_percent': cache_hit_rate,
                'total_errors': sum(self.error_count.values()),
                'endpoint_stats': self._get_endpoint_stats(),
                'health_status': self._get_health_status(avg_response_time, success_rate)
            }

    def _get_endpoint_stats(self) -> Dict:
        """Get statistics per endpoint"""
        stats = {}

        for endpoint, calls in self.api_calls.items():
            if calls:
                durations = [call['duration'] for call in calls]
                successes = [call['success'] for call in calls]

                stats[endpoint] = {
                    'total_calls': len(calls),
                    'avg_duration_ms': sum(durations) / len(durations) * 1000,
                    'success_rate': sum(successes) / len(successes) * 100,
                    'errors': self.error_count[endpoint]
                }

        return stats

    def _get_health_status(self, avg_response_time: float, success_rate: float) -> str:
        """Determine system health status"""
        if success_rate < 90:
            return 'critical'
        elif avg_response_time > 5.0 or success_rate < 95:
            return 'warning'
        else:
            return 'healthy'

    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"logs/performance_metrics_{timestamp}.json"

        stats = self.get_performance_stats()

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        return filename

    def get_real_time_metrics(self) -> Dict:
        """Get real-time metrics for dashboard"""
        with self._lock:
            # Last 10 requests
            recent = list(self.request_times)[-10:]

            return {
                'current_rps': len([r for r in recent if time.time() - r['timestamp'] < 10]),
                'latest_response_time': recent[-1]['duration'] * 1000 if recent else 0,
                'active_connections': 1,  # Simplified for this implementation
                'memory_usage_mb': self._get_memory_usage(),
                'timestamp': time.time()
            }

    def _get_memory_usage(self) -> float:
        """Get approximate memory usage"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except ImportError:
            return 0.0


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def monitor_performance(endpoint: str):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise e
            finally:
                duration = time.time() - start_time
                perf_monitor.log_request(endpoint, duration, success)

        return wrapper
    return decorator


if __name__ == "__main__":
    # Test performance monitor
    monitor = PerformanceMonitor()

    # Simulate some requests
    import random

    for i in range(50):
        endpoint = random.choice(
            ['/api/agent_chat', '/api/agent_stats', '/api/semantic_search'])
        duration = random.uniform(0.1, 2.0)
        success = random.choice([True, True, True, False])  # 75% success rate

        monitor.log_request(endpoint, duration, success)
        time.sleep(0.01)

    # Print stats
    stats = monitor.get_performance_stats()
    print(json.dumps(stats, indent=2))

    # Export metrics
    filename = monitor.export_metrics()
    print(f"Metrics exported to: {filename}")
