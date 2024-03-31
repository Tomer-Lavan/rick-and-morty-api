from typing import Any, Dict


class Cache:
    """
    A Singelton simple cache class for the api. 
    Currently support only the rick and morty api service but can be extended to other services.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._cache: Dict[str, Any] = {}
        return cls._instance

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def clear(self) -> None:
        self._cache.clear()
