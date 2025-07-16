# Redis Basic Operations

This repository contains Python scripts that demonstrate various Redis operations including caching, call tracking, and web page caching with expiration.

## Tasks

### 0. Writing strings to Redis
**File:** `exercise.py`  
**Description:**  
- Implements a `Cache` class that stores data in Redis with randomly generated keys
- The `store` method accepts strings, bytes, numbers and returns the generated key
- Uses `uuid` for key generation and flushes Redis on initialization

**Usage:**
```python
cache = Cache()
key = cache.store("hello")
print(cache.get(key))  # b'hello'