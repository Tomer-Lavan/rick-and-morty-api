from functools import wraps
from typing import Callable, Any
from app.services.cache import Cache

cache = Cache()


def cache_data(key_format: str):
    """
    A decorator to cache the result of an async function based on a formatted key.
    Args:
        key_format (str): A format string used to create the cache key.
    Returns:
        Callable: A decorator that wraps an async function and caches its result.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Format the cache key based on the function's arguments from rick and morty api service.
            params_str = "None" if "params" not in kwargs or kwargs['params'] is None else str(
                kwargs['params'])
            endpoint_str = args[0] if args else "None"
            ids_str = "None" if "ids" not in kwargs or kwargs['ids'] is None else str(
                kwargs['ids'])
            formatted_key = key_format.format(
                endpoint=endpoint_str, params=params_str, ids=ids_str)

            # Check if the result is already cached
            cached_data = cache.get(formatted_key)
            if cached_data is not None:
                return cached_data

            # If not cached, call the function and cache its result
            data = await func(*args, **kwargs)

            cache.set(formatted_key, data)
            return data
        return wrapper
    return decorator
