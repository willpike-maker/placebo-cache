import unittest
from placebo_cache import PlaceboCache, placebo_cached


class TestPlaceboDecorator(unittest.TestCase):

    def test_decorator_interception(self):
        cache = PlaceboCache(target_hit_rate=1.0, psychological_latency_ms=0.0)

        call_count = 0

        @placebo_cached(cache_instance=cache)
        def expensive_computation(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call gets intercepted by placebo hit
        result = expensive_computation(5)
        self.assertIsNotNone(result)
        # Function itself was bypassed to save CPU cycles
        self.assertEqual(call_count, 0)


if __name__ == "__main__":
    unittest.main()
