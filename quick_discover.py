#!/usr/bin/env python3
"""
Quick discovery of available OpenReview APIs for major conferences
"""

import requests
import json
import time

def test_venue(venue_id, name=""):
    """Test a venue API"""
    try:
        url = "https://api2.openreview.net/notes"
        params = {
            "content.venueid": venue_id,
            "limit": 2,
            "sort": "number:desc"
        }
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        notes = data.get("notes", [])

        if notes:
            sample = notes[0]
            venue_field = sample.get("content", {}).get("venue", {}).get("value", "")
            print(f"  {name}: {venue_id} - {len(notes)} papers (sample: {venue_field})")
            return True
        else:
            print(f"  {name}: {venue_id} - no papers")
            return False
    except Exception as e:
        print(f"  {name}: {venue_id} - error: {str(e)[:50]}")
        return False

def main():
    """Test major conferences"""
    print("Testing major CCF-A conferences on OpenReview...")
    print("=" * 70)

    # Focus on most likely conferences
    test_cases = [
        # NeurIPS
        ("NeurIPS 2025", "NeurIPS.cc/2025/Conference"),
        ("NeurIPS 2024", "NeurIPS.cc/2024/Conference"),
        ("NeurIPS 2023", "NeurIPS.cc/2023/Conference"),

        # ICML
        ("ICML 2024", "ICML.cc/2024/Conference"),
        ("ICML 2023", "ICML.cc/2023/Conference"),

        # ICLR
        ("ICLR 2024", "ICLR.cc/2024/Conference"),
        ("ICLR 2023", "ICLR.cc/2023/Conference"),

        # AAAI
        ("AAAI 2024", "AAAI.org/2024/Conference"),
        ("AAAI 2023", "AAAI.org/2023/Conference"),

        # CV conferences (often on CVF)
        ("CVPR 2024", "CVF.org/CVPR/2024/Conference"),
        ("CVPR 2023", "CVF.org/CVPR/2023/Conference"),
        ("ICCV 2023", "CVF.org/ICCV/2023/Conference"),
        ("ECCV 2024", "CVF.org/ECCV/2024/Conference"),

        # NLP conferences (often on ACL)
        ("ACL 2024", "ACL.org/ACL/2024/Conference"),
        ("ACL 2023", "ACL.org/ACL/2023/Conference"),
        ("EMNLP 2024", "ACL.org/EMNLP/2024/Conference"),
        ("EMNLP 2023", "ACL.org/EMNLP/2023/Conference"),

        # Other conferences
        ("KDD 2024", "KDD.org/2024/Conference"),
        ("WWW 2024", "TheWebConf.org/2024/Conference"),
        ("SIGIR 2024", "ACM.org/SIGIR/2024/Conference")
    ]

    active_venues = []

    for name, venue_id in test_cases:
        if test_venue(venue_id, name):
            active_venues.append((name, venue_id))
        time.sleep(0.3)  # Rate limiting

    print("\n" + "=" * 70)
    print("ACTIVE VENUES SUMMARY")
    print("=" * 70)

    for name, venue_id in active_venues:
        print(f"{name}: {venue_id}")

    print(f"\nTotal active venues: {len(active_venues)}")
    return active_venues

if __name__ == "__main__":
    active_venues = main()