#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def track_and_cache(method: Callable) -> Callable:
    """Decorator to track URL access counts and cache results"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that implements tracking and caching"""
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        # Increment access count
        redis_client.incr(count_key)

        # Check if cached content exists
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Get the page content if not cached
        content = method(url)

        # Cache the content with 10-second expiration
        redis_client.setex(cache_key, 10, content)
        
        return content
    return wrapper

@track_and_cache
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL"""
    response = requests.get(url)
    return response.text