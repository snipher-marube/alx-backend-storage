#!/usr/bin/env python3
"""
Redis basic exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional

class Cache:
    """Cache class for storing data in Redis"""
    
    def __init__(self):
        """Initialize the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key and return the key
        
        Args:
            data: Data to store (str, bytes, int, or float)
            
        Returns:
            str: The generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key