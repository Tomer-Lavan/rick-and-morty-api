from functools import wraps
from typing import Callable, Any
from app.services.cache import Cache

cache = Cache()


def cache_data(key_format: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            params_str = "None" if "params" not in kwargs or kwargs['params'] is None else str(
                kwargs['params'])
            endpoint_str = args[0] if args else "None"
            ids_str = "None" if "ids" not in kwargs or kwargs['ids'] is None else str(
                kwargs['ids'])
            formatted_key = key_format.format(
                endpoint=endpoint_str, params=params_str, ids=ids_str)

            cached_data = cache.get(formatted_key)
            if cached_data is not None:
                return cached_data

            data = await func(*args, **kwargs)

            cache.set(formatted_key, data)
            return data
        return wrapper
    return decorator
