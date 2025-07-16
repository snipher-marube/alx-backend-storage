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

    def retrieve(self, key: str) -> Optional[Union[str, bytes, int, float]]:
        """Retrieve data from Redis by key
        
        Args:
            key: The key to retrieve data for
            
        Returns:
            Optional[Union[str, bytes, int, float]]: The retrieved data or None if not found
        """
        return self._redis.get(key)

    def delete(self, key: str) -> bool:
        """Delete data from Redis by key
        
        Args:
            key: The key to delete data for
            
        Returns:
            bool: True if the key was deleted, False otherwise
        """
        return self._redis.delete(key) > 0

    def execute(self, func: Callable, *args, **kwargs) -> Optional[Union[str, bytes, int, float]]:
        """Execute a function with Redis connection
        
        Args:
            func: The function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Optional[Union[str, bytes, int, float]]: The result of the function execution
        """
        return func(self._redis, *args, **kwargs) if callable(func) else None