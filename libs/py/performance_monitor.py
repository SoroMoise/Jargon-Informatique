#!/usr/bin/python3
# coding : utf-8

import time
import psutil
import os
from functools import wraps

class PerformanceMonitor:
    """
    Simple performance monitoring for the app
    """
    
    def __init__(self):
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())
    
    def get_memory_usage(self) -> dict:
        """Get current memory usage"""
        memory_info = self.process.memory_info()
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': self.process.memory_percent()
        }
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        return self.process.cpu_percent()
    
    def get_uptime(self) -> float:
        """Get app uptime in seconds"""
        return time.time() - self.start_time
    
    def log_performance(self, context: str = ""):
        """Log current performance metrics"""
        memory = self.get_memory_usage()
        cpu = self.get_cpu_usage()
        uptime = self.get_uptime()
        
        print(f"[PERF] {context} - Memory: {memory['rss']:.1f}MB ({memory['percent']:.1f}%), "
              f"CPU: {cpu:.1f}%, Uptime: {uptime:.1f}s")

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            if execution_time > 0.1:  # Only log slow operations
                print(f"[PERF] {func.__name__} took {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"[PERF] {func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    return wrapper

# Global instance
perf_monitor = PerformanceMonitor()