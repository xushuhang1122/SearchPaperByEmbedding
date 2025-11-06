#!/usr/bin/env python3
"""
Test decision patterns for different conferences
"""

import requests
import json
import time

def test_decision_pattern(venue_id, pattern, limit=3):
    """Test a specific decision pattern for a venue"""
    try:
        url = "https://api2.openreview.net/notes"
        params = {
            "content.venueid": venue_id,
            "content.venue": pattern,
            "limit": limit,
            "sort": "number:desc"
        }
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        notes = data.get("notes", [])

        return len(notes)
    except Exception as e:
        print(f"Error testing {pattern}: {e}")
        return 0

def discover_decision_patterns():
    """Discover decision patterns for active conferences"""
    print("Discovering decision patterns for active conferences...")
    print("=" * 60)

    # Active venues from previous test
    venues = {
        "NeurIPS 2025": "NeurIPS.cc/2025/Conference",
        "NeurIPS 2024": "NeurIPS.cc/2024/Conference",
        "NeurIPS 2023": "NeurIPS.cc/2023/Conference",
        "ICML 2024": "ICML.cc/2024/Conference",
        "ICML 2023": "ICML.cc/2023/Conference",
        "ICLR 2024": "ICLR.cc/2024/Conference"
    }

    # Common decision patterns to test
    base_patterns = [
        "oral", "spotlight", "poster", "accept", "reject"
    ]

    conference_patterns = {}

    for conf_name, venue_id in venues.items():
        print(f"\nTesting {conf_name}...")

        # Extract conference name and year
        parts = conf_name.split()
        conf = parts[0]
        year = parts[1]

        active_patterns = {}

        # Test patterns
        test_patterns = [
            f"{conf} {year} oral",
            f"{conf} {year} spotlight",
            f"{conf} {year} poster",
            f"{conf} {year} accept",
            f"{conf} {year} reject",
            # Case variations
            f"{conf} {year} Oral",
            f"{conf} {year} Poster",
            f"{conf} {year} Spotlight",
        ]

        for pattern in test_patterns:
            count = test_decision_pattern(venue_id, pattern, limit=2)
            if count > 0:
                active_patterns[pattern] = count
                print(f"  [OK] {pattern}: {count} papers")
            else:
                print(f"  [..] {pattern}: {count} papers")

            time.sleep(0.2)

        conference_patterns[conf_name] = {
            "venue_id": venue_id,
            "patterns": active_patterns
        }

    print("\n" + "=" * 60)
    print("DISCOVERED PATTERNS SUMMARY")
    print("=" * 60)

    for conf_name, info in conference_patterns.items():
        print(f"\n{conf_name} ({info['venue_id']}):")
        if info['patterns']:
            for pattern, count in info['patterns'].items():
                print(f"  {pattern}: {count}+ papers")
        else:
            print("  No specific patterns found")

    return conference_patterns

if __name__ == "__main__":
    patterns = discover_decision_patterns()