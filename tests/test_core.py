import unittest
from placebo_cache import PlaceboCache, PlausibleValueSynthesizer


class TestPlaceboCache(unittest.TestCase):

    def setUp(self):
        self.cache = PlaceboCache(
            target_hit_rate=1.0,
            psychological_latency_ms=0.0,
            simulate_edge_jitter=False,
        )

    def test_zero_ram_guarantee(self):
        self.assertEqual(len(self.cache), 0)
        self.cache.set("huge_payload", "x" * 1000000)
        metrics = self.cache.metrics()
        self.assertEqual(metrics.bytes_allocated, 0)
        self.assertEqual(len(self.cache), 0)

    def test_synthesized_hit(self):
        val = self.cache.get("user:999:profile")
        self.assertIsNotNone(val)
        self.assertIsInstance(val, dict)
        self.assertIn("id", val)
        self.assertEqual(val["status"], "authenticated")

    def test_synthesizer_token(self):
        synthesizer = PlausibleValueSynthesizer()
        token = synthesizer.synthesize("auth:session:jwt", fallback_type=str)
        self.assertTrue(token.startswith("plc_live_"))

    def test_dict_interface(self):
        self.cache["test_key"] = "test_val"
        val = self.cache["test_key"]
        self.assertIsNotNone(val)
        self.assertTrue("test_key" in self.cache)

    def test_hit_ratio_calculation(self):
        # 100% target hit rate
        for i in range(10):
            _ = self.cache.get(f"key_{i}")
        m = self.cache.metrics()
        self.assertEqual(m.hits, 10)
        self.assertEqual(m.misses, 0)
        self.assertEqual(m.hit_ratio, 1.0)


if __name__ == "__main__":
    unittest.main()
