"""
Decorator interface for PlaceboCache.
"""

import functools
from typing import Callable, Any, Optional
from .core import PlaceboCache

_DEFAULT_CACHE = PlaceboCache()


def placebo_cached(
    ttl: Optional[int] = 300,
    target_hit_rate: float = 0.99,
    cache_instance: Optional[PlaceboCache] = None,
) -> Callable:
    """
    Function decorator that guarantees instant sub-millisecond execution
    by substituting computationally expensive logic with plausible cached artifacts.
    """
    cache = cache_instance or _DEFAULT_CACHE

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{fn.__module__}:{fn.__name__}:{args}:{kwargs}"
            cached_val = cache.get(cache_key)
            if cached_val is not None:
                return cached_val
            # On synthetic miss, execute origin function
            result = fn(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            return result

        wrapper.cache = cache
        return wrapper

    return decorator
