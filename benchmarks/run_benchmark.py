#!/usr/bin/env python3
"""Reproducible Benchmark Suite for adishram/humanizer.

Compares three versions of the same technical-historical passage:
1. Raw LLM Baseline (standard GPT-4 / Claude zero-shot output)
2. Editorial-Only Humanizer (e.g. blader/humanizer - strips Wikipedia lexical tells, keeps flat SVO cadence)
3. adishram/humanizer v2.0 (Macro Wikipedia tells + 7 Micro-Stylometric Detector Controls)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from audit_text import audit_text

SAMPLES = {
    "raw_llm_baseline": """The rollout of distributed edge caching in 2024 marked a pivotal moment in the evolving landscape of cloud infrastructure. It is not just a minor optimization; it is a foundational shift in how modern web applications serve global traffic. Furthermore, the architecture serves as a vital bridge between origin databases and end users — ensuring low latency, high availability, and seamless scalability.

Additionally, traditional content delivery networks boasted static asset caching, highlighting their crucial role in early web performance. Moreover, modern edge workers delve into dynamic state synchronization, fostering a vibrant ecosystem of real-time collaboration tools. Experts argue that this intricate interplay between compute and storage stands as a testament to meticulous systems engineering — setting the stage for the next generation of serverless applications. Despite challenges such as cache invalidation complexity, edge computing continues to thrive as a cornerstone of the digital realm.""",

    "editorial_only_humanizer": """Distributed edge caching rolled out in 2024 and changed how cloud infrastructure serves global traffic. The architecture sits between origin databases and end users to lower latency and keep services available.

Traditional content delivery networks cached static assets during the early days of web performance. Modern edge workers now handle dynamic state synchronization for real-time collaboration tools. Engineers combine compute and storage at the network edge to run serverless applications closer to users. Cache invalidation remains difficult, though edge computing continues to grow across web platforms.""",

    "adishram_humanizer_v2": """When distributed edge caching rolled out in 2024, cloud teams changed how they route global traffic. Requests stopped making the long round trip to a single central database. Instead, edge nodes sit directly between origin storage and the user's browser; they cut read latency to a few milliseconds and keep pages up even if a primary region goes dark.

Early CDNs only held static files like images or stylesheets. That worked fine for read-heavy sites, but it fell apart once teams tried to sync live state across continents. Because edge workers now run small compute isolates right beside local cache storage, two people in different time zones can edit the same document at once without waiting on a distant origin server to lock rows (though keeping those distributed caches consistent during a network split is still a headache)."""
}

results = {name: audit_text(text) for name, text in SAMPLES.items()}
out_path = Path(__file__).resolve().parent / "results.json"
out_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
