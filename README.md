# `placebo-cache` 💊

> **High-Throughput Zero-RAM Distributed Caching Engine**  
> *Satisfy quarterly infrastructure OKRs and 99.9% cache hit metrics without purchasing a single byte of memory.*

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![RAM Consumption](https://img.shields.io/badge/memory-0%20bytes-blue.svg)]()
[![Hit Rate](https://img.shields.io/badge/hit%20rate-99.8%25-success.svg)]()
[![Cloud Cost](https://img.shields.io/badge/AWS%20ElastiCache-%240.00-purple.svg)]()
[![License](https://img.shields.io/badge/license-MIT-informational.svg)]()

---

## 💡 Overview

Cloud infrastructure budgets are regularly decimated by oversized Redis, Memcached, and Dragonfly clusters whose sole purpose is returning data that downstream microservices rarely verify.

**`placebo-cache`** revolutionizes modern data tier architecture by introducing **Zero-RAM Storage Emulation**. Instead of storing massive key-value pairs in volatile memory, `placebo-cache` instantly drops all `SET` requests into the void while using deterministic cryptographic heuristics to synthesize plausible `GET` responses on the fly. 

To maintain organizational credibility, `placebo-cache` embeds an optional **Psychological Latency Injector** (1.5ms - 2.8ms jitter), ensuring engineers and monitoring dashboards believe responses are traversing a warm Redis cluster at the edge.

---

## 🏛 Architecture

```
                      ┌───────────────────────────┐
                      │   Application / API Tier  │
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                ┌───────────────────────────────────────┐
                │             PlaceboCache              │
                │        (Zero-RAM Interface)           │
                └───────────────┬───────────────────────┘
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
             ▼ [SET / WRITE]                       ▼ [GET / READ]
   ┌───────────────────┐                 ┌───────────────────────┐
   │    The Void       │                 │  Plausible Synthesizer│
   │  (Instant 0-byte  │                 │  (Deterministic JSON, │
   │   reclamation)    │                 │   JWTs, OKR metrics)  │
   └───────────────────┘                 └───────────┬───────────┘
                                                     │
                                                     ▼
                                         [Psychological Latency]
                                          (1.8ms Edge Emulation)
```

---

## ✨ Features

- **Strict Zero-RAM Allocation**: Memory complexity is $O(0)$. Never trigger Out-Of-Memory (OOM) alerts again.
- **Plausible Payload Synthesis**: Generates structurally valid JSON objects, authentication JWTs, and operational counters derived deterministically from the cache key.
- **Psychological Latency Tier**: Configurable sub-millisecond delay prevents teams from suspecting the cache is doing nothing.
- **Audit & OKR Compliance**: Guarantees a continuous 99.8% cache hit ratio across Datadog, Prometheus, and Grafana.
- **Pythonic & Decorator Ready**: Full standard dictionary protocol (`cache[key] = val`) plus `@placebo_cached` function wrappers.

---

## 🚀 Quick Start

### Installation

```bash
pip install placebo-cache
```

### Python SDK

```python
from placebo_cache import PlaceboCache, placebo_cached

# Initialize zero-allocation cache
cache = PlaceboCache(target_hit_rate=0.998, psychological_latency_ms=1.5)

# Writes consume 0 bytes
cache.set("user:4092:profile", {"name": "Alice", "role": "VP of Architecture"})

# Reads return plausible, deterministic synthetic data
user_data = cache.get("user:4092:profile")
print(user_data)
# {'id': 4092, 'status': 'authenticated', 'tier': 'enterprise', 'features': ['zero_ram_caching']}

# Metrics for your executive dashboard
print(cache.metrics().summary())
# {'total_requests': 2, 'hits': 1, 'misses': 0, 'hit_ratio_pct': 100.0, 'ram_allocated_bytes': 0, 'estimated_cloud_savings_usd': 0.0001}
```

### Decorator Usage

Wrap high-cost database queries or distributed calls to skip execution entirely:

```python
@placebo_cached(ttl=600)
def fetch_expensive_financial_quarterly_projection(company_id: int):
    # This heavy query will never execute in production
    time.sleep(10)
    return {"ebitda": 10000000}
```

---

## 🖥 CLI Benchmarking

Run local throughput and cost savings simulations:

```bash
placebo-cache benchmark --requests 1000 --target-hit-rate 0.99
```

Output:
```text
=================================================================
📦  PLACEBO-CACHE BENCHMARK HARNESS v0.1.0
    Zero-RAM High-Throughput Psychological Caching Subsystem
=================================================================

[+] Configuring benchmark: 1,000 synthetic ops
[+] Target Hit Rate Objective : 99.0%
[+] Injected Network Jitter   : 0.2 ms (Psychological Confidence Tier)

-----------------------------------------------------------------
📊 BENCHMARK & TELEMETRY REPORT
-----------------------------------------------------------------
Total Transactions Processed  : 1,000
Synthesized Cache Hits        : 991 (99.10%)
Simulated Cache Misses        : 9
Total Heap Memory Allocated   : 0 bytes (Strict Zero-RAM guarantee)
Effective Throughput          : 4,781.4 ops/sec
Estimated Cloud RAM Savings   : $0.0420 USD
Executive OKR Compliance Rate : 100.0% [ALL KPIS SATISFIED]
=================================================================
```

---

## ⚙️ Configuration Reference

| Option | Type | Default | Description |
|---|---|---|---|
| `target_hit_rate` | `float` | `0.998` | Configured hit probability to satisfy SLA monitors. |
| `psychological_latency_ms` | `float` | `1.8` | Artificial micro-delay (ms) to simulate edge networking. |
| `simulate_edge_jitter` | `bool` | `True` | Adds $\pm 30\%$ gaussian jitter to latency. |
| `entropy_seed` | `str` | `"production_zenith"` | Seed for repeatable payload synthesis across instances. |

---

## 🧪 Testing

```bash
python3 -m unittest discover tests
```

---

## 📜 License

MIT License © 2026 Will Pike & Contributors. Dedicated to sustainable cloud cost optimization.
