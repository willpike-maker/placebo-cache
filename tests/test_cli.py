import unittest
import io
import sys
from placebo_cache.cli import run_benchmark, run_inspect


class TestPlaceboCLI(unittest.TestCase):

    def test_benchmark_run(self):
        buf = io.StringIO()
        orig_stdout = sys.stdout
        try:
            sys.stdout = buf
            run_benchmark(requests_count=20, hit_rate=1.0, latency=0.0)
        finally:
            sys.stdout = orig_stdout

        out = buf.getvalue()
        self.assertIn("PLACEBO-CACHE BENCHMARK HARNESS", out)
        self.assertIn("Total Heap Memory Allocated   : 0 bytes", out)
        self.assertIn("ALL KPIS SATISFIED", out)

    def test_inspect_run(self):
        buf = io.StringIO()
        orig_stdout = sys.stdout
        try:
            sys.stdout = buf
            run_inspect("user:42:profile")
        finally:
            sys.stdout = orig_stdout

        out = buf.getvalue()
        self.assertIn("Key: user:42:profile", out)
        self.assertIn("Synthesized Cache Value", out)


if __name__ == "__main__":
    unittest.main()
