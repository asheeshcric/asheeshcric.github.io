#!/usr/bin/env python3
"""
Fetches live citation counts from Semantic Scholar API and patches index.html.
Runs weekly via GitHub Actions (full internet access).
Uses exponential backoff + optional S2_API_KEY env var for higher rate limits.
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

S2_BASE  = "https://api.semanticscholar.org/graph/v1"
API_KEY  = os.environ.get("S2_API_KEY", "")
HEADERS  = {
    "User-Agent": "jashish.com.np-citation-bot/1.0 (ashiz2013@gmail.com)",
    **({"x-api-key": API_KEY} if API_KEY else {}),
}
# Polite delay between requests (S2 free tier: ~1 req/sec; with key: 10 req/sec)
DELAY = 1.2 if API_KEY else 3.0

# ── Paper registry ─────────────────────────────────────────────────────────────
# badge_marker: the current text inside <span class="pub-badge">...</span>
# s2id: direct Semantic Scholar paper ID (preferred — no search quota)
# query: fallback title search if s2id is missing or fails
PAPERS = [
    {
        "badge_marker": "2,304 citations",
        "s2id": "b28f3e2c01b37d68985c04b5baea33869dded619",  # SSL Survey (Technologies 2020)
    },
    {
        "badge_marker": "28 citations",
        "query": "Smart Sensor Suit SSS Cognitive Physical Fatigue Machine Learning Jaiswal HCII 2023",
    },
    {
        "badge_marker": "15 citations",
        "query": "Understanding Cognitive Fatigue fMRI Scans Self-supervised Learning Jaiswal 2021",
    },
    {
        "badge_marker": "3 citations",
        "query": "SmartFunction Immersive VR Assess Attention Embodied Cognition Jaiswal PETRA 2023",
    },
    {
        "badge_marker": "1 citation",
        "query": "Assistive Robotic System Cognitive State Assessment Spinal Cord Injury Jaiswal PETRA 2024",
    },
    {
        "badge_marker": "502 citations",
        "query": "Review Extended Reality XR Technologies Manufacturing Training Doolani Technologies 2020",
    },
    {
        "badge_marker": "40 citations",
        "query": "Examining Landscape Cognitive Fatigue Detection Comprehensive Survey Karim Technologies 2024",
    },
    {
        "badge_marker": "33 citations",
        "s2id": "13f8db4655e6263443490e7b491f0a1d25e69461",  # HAND-REHA (confirmed above)
    },
    {
        "badge_marker": "24 citations",
        "query": "Light-weight Seated Posture Guidance Machine Learning Computer Vision Kapoor Jaiswal PETRA 2022",
    },
    {
        "badge_marker": "20 citations",
        "query": "Self-Supervised Human Activity Recognition Augmenting Generative Adversarial Networks Zadeh Jaiswal 2021",
    },
]


def s2_get(url: str, retries: int = 6) -> dict | None:
    """GET with exponential backoff on 429."""
    backoff = DELAY
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = backoff * (2 ** attempt)
                print(f"    429 — waiting {wait:.0f}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            else:
                print(f"    HTTP {e.code}")
                return None
        except Exception as e:
            print(f"    Error: {e}")
            return None
    print("    Exhausted retries")
    return None


def fetch_by_id(s2id: str) -> int | None:
    url  = f"{S2_BASE}/paper/{s2id}?fields=citationCount"
    data = s2_get(url)
    if data and "citationCount" in data:
        return data["citationCount"]
    return None


def fetch_by_search(query: str) -> int | None:
    url  = (f"{S2_BASE}/paper/search"
            f"?query={urllib.parse.quote(query)}"
            f"&fields=title,citationCount&limit=1")
    data = s2_get(url)
    if data and data.get("data"):
        result = data["data"][0]
        print(f"    matched: {result.get('title','')[:60]}")
        return result.get("citationCount")
    return None


def format_count(n: int) -> str:
    return f"{n:,} citation{'s' if n != 1 else ''}"


def main():
    html_path = Path(__file__).parent.parent / "index.html"
    content   = html_path.read_text()
    updated   = 0

    for paper in PAPERS:
        marker = paper["badge_marker"]
        print(f"\nFetching [{marker}]...")
        count = None

        # Direct ID lookup first — faster, more reliable
        if paper.get("s2id"):
            count = fetch_by_id(paper["s2id"])
            if count is not None:
                print(f"  via ID → {count:,}")
            time.sleep(DELAY)

        # Fallback: title search
        if count is None and paper.get("query"):
            count = fetch_by_search(paper["query"])
            if count is not None:
                print(f"  via search → {count:,}")
            time.sleep(DELAY)

        if count is None:
            print(f"  not found — keeping static value")
            continue

        new_badge = format_count(count)
        old_span  = f'<span class="pub-badge">{marker}</span>'
        new_span  = f'<span class="pub-badge">{new_badge}</span>'

        if old_span in content:
            content = content.replace(old_span, new_span, 1)
            print(f"  patched: '{marker}' → '{new_badge}'")
            updated += 1
        else:
            print(f"  WARNING: marker not found in HTML — skipping")

    # ── Author-level totals: hero citations stat + h-index ────────────────────
    print("\n\nFetching author profile totals...")
    time.sleep(DELAY * 2)

    # Search by name + affiliation
    for query in ["Ashish Jaiswal Meta Facebook", "Ashish Jaiswal UT Arlington"]:
        url  = (f"{S2_BASE}/author/search"
                f"?query={urllib.parse.quote(query)}"
                f"&fields=name,citationCount,hIndex,paperCount&limit=5")
        data = s2_get(url)
        if not data or not data.get("data"):
            continue

        # Pick the author with the most citations (most likely to be Ashish)
        candidates = [a for a in data["data"] if a.get("citationCount", 0) > 100]
        if not candidates:
            continue
        best  = max(candidates, key=lambda a: a.get("citationCount", 0))
        total = best.get("citationCount", 0)
        h     = best.get("hIndex", 0)
        print(f"  Found: {best.get('name')} | {total:,} citations | h-index {h}")

        # Update hero stat value
        content = re.sub(
            r'(<p class="stat-value">)[\d,]+\+?(</p>\s*<p class="stat-label">Citations)',
            lambda m: f'{m.group(1)}{total:,}+{m.group(2)}',
            content,
        )
        # Update h-index wherever it appears
        content = re.sub(r'h-index \d+', f'h-index {h}', content)
        print(f"  Hero stat → {total:,}+ | h-index → {h}")
        break

    html_path.write_text(content)
    print(f"\n✓ Done. Updated {updated}/{len(PAPERS)} paper badges.")


if __name__ == "__main__":
    main()
