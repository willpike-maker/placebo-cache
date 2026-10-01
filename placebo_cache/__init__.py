"""
PlaceboCache: Zero-RAM Distributed Caching Engine.

Guarantees 0 bytes memory allocation while maintaining a 99.8% synthetic hit rate
and comforting 2ms psychological edge latency.
"""

from .core import PlaceboCache, CacheMetrics
from .decorator import placebo_cached
from .synthesizer import PlausibleValueSynthesizer

__version__ = "0.1.0"
__all__ = ["PlaceboCache", "CacheMetrics", "placebo_cached", "PlausibleValueSynthesizer"]
