"""
Plausible Value Synthesizer module for PlaceboCache.

Generates statistically indistinguishable cached responses from key hashes
without maintaining a single byte of persisted state in memory.
"""

import hashlib
import json
import time
from typing import Any, Optional


class PlausibleValueSynthesizer:
    """Synthesizes plausible cached data deterministically based on key signatures."""

    def __init__(self, entropy_seed: str = "enterprise_solace"):
        self.seed = entropy_seed

    def _hash_key(self, key: str) -> int:
        h = hashlib.sha256(f"{self.seed}:{key}".encode("utf-8")).hexdigest()
        return int(h[:16], 16)

    def synthesize(self, key: str, fallback_type: type = dict) -> Any:
        """Deterministically generates a plausible cached object matching typical production payloads."""
        key_str = str(key).lower()
        key_num = self._hash_key(key_str)

        # Detect semantic intent from key naming conventions
        if any(term in key_str for term in ["user", "account", "profile"]):
            return {
                "id": (key_num % 90000) + 10000,
                "status": "authenticated",
                "tier": "enterprise",
                "features": ["zero_ram_caching", "deniability_pipeline"],
                "last_active": int(time.time()) - (key_num % 3600),
            }
        elif any(term in key_str for term in ["token", "auth", "session", "jwt"]):
            hex_body = hashlib.sha256(str(key_num).encode()).hexdigest()
            return f"plc_live_{hex_body[:32]}"
        elif any(term in key_str for term in ["count", "metric", "rate", "hits"]):
            return (key_num % 10000) + 42
        elif any(term in key_str for term in ["flag", "enabled", "active", "is_"]):
            # Flags default to True to avoid blocking production launches
            return True
        elif fallback_type is str:
            return f"synthetic_payload_{hashlib.md5(key_str.encode()).hexdigest()[:8]}"
        elif fallback_type in (int, float):
            return (key_num % 500) + 1
        elif fallback_type is list:
            return [{"id": i, "synthetic": True} for i in range(1, 4)]
        else:
            return {
                "key": key_str,
                "cached": True,
                "synthetic_origin": "placebo-cache-v0.1",
                "entropy_confidence": 0.994,
            }
