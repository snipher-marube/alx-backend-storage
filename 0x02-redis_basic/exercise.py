#!/usr/bin/env python3
"""
Redis basic exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorator"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorator"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        
        # Execute the method and store its output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        
        return output
    return wrapper

def replay(method: Callable) -> None:
    """Display the history of calls of a particular function"""
    r = method.__self__._redis
    method_name = method.__qualname__
    
    # Get call count
    call_count = r.get(method_name).decode('utf-8') if r.get(method_name) else '0'
    print(f"{method_name} was called {call_count} times:")
    
    # Get inputs and outputs
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    
    # Display each call's input and output
    for input_data, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output.decode('utf-8')}")

class Cache:
    """Cache class for storing data in Redis"""
    
    def __init__(self):
        """Initialize the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get data from Redis and optionally apply conversion function
        
        Args:
            key: Key to retrieve
            fn: Optional conversion function
            
        Returns:
            Original data in the appropriate format
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Get a string value from Redis
        
        Args:
            key: Key to retrieve
            
        Returns:
            str: The decoded string
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get an integer value from Redis
        
        Args:
            key: Key to retrieve
            
        Returns:
            int: The integer value
        """
        return self.get(key, lambda d: int(d))