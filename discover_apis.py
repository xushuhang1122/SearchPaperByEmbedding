#!/usr/bin/env python3
"""
Discover available OpenReview API endpoints for different conferences and years
"""

import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

def test_venue_api(venue_id, limit=3):
    """Test if a venue API is accessible and has papers"""
    url = "https://api2.openreview.net/notes"
    params = {
        "content.venueid": venue_id,
        "limit": limit,
        "sort": "number:desc"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        notes = data.get("notes", [])

        if notes:
            # Check if papers have decision information
            sample_note = notes[0]
            venue_field = sample_note.get("content", {}).get("venue", {}).get("value", "")
            return {
                "venue_id": venue_id,
                "papers_count": len(notes),
                "sample_venue": venue_field,
                "status": "active"
            }
        else:
            return {
                "venue_id": venue_id,
                "papers_count": 0,
                "sample_venue": "",
                "status": "empty"
            }
    except Exception as e:
        return {
            "venue_id": venue_id,
            "papers_count": 0,
            "sample_venue": "",
            "status": f"error: {str(e)}"
        }

def discover_conferences():
    """Discover available conferences and their API endpoints"""

    # Define conference patterns for CCF-A conferences
    conferences = {
        "NeurIPS": ["NeurIPS.cc/2025/Conference", "NeurIPS.cc/2024/Conference", "NeurIPS.cc/2023/Conference"],
        "ICML": ["ICML.cc/2025/Conference", "ICML.cc/2024/Conference", "ICML.cc/2023/Conference"],
        "ICLR": ["ICLR.cc/2025/Conference", "ICLR.cc/2024/Conference", "ICLR.cc/2023/Conference"],
        "AAAI": ["AAAI.org/2025/Conference", "AAAI.org/2024/Conference", "AAAI.org/2023/Conference"],
        "CVPR": ["CVF.org/CVPR/2025/Conference", "CVF.org/CVPR/2024/Conference", "CVF.org/CVPR/2023/Conference"],
        "ICCV": ["CVF.org/ICCV/2023/Conference", "CVF.org/ICCV/2021/Conference"],
        "ECCV": ["CVF.org/ECCV/2024/Conference", "CVF.org/ECCV/2022/Conference"],
        "ACL": ["ACL.org/ACL/2024/Conference", "ACL.org/ACL/2023/Conference"],
        "EMNLP": ["ACL.org/EMNLP/2024/Conference", "ACL.org/EMNLP/2023/Conference"],
        "KDD": ["KDD.org/2024/Conference", "KDD.org/2023/Conference"],
        "WWW": ["TheWebConf.org/2024/Conference", "TheWebConf.org/2023/Conference"],
        "SIGIR": ["ACM.org/SIGIR/2024/Conference", "ACM.org/SIGIR/2023/Conference"]
    }

    results = {}

    print("Discovering OpenReview API endpoints...")
    print("=" * 60)

    all_venue_ids = []
    for conf, venue_ids in conferences.items():
        all_venue_ids.extend(venue_ids)
        print(f"{conf}: {len(venue_ids)} venue IDs to test")

    # Test venues with some delay to avoid rate limiting
    active_venues = []
    for i, venue_id in enumerate(all_venue_ids):
        print(f"\nTesting [{i+1}/{len(all_venue_ids)}]: {venue_id}")
        result = test_venue_api(venue_id)

        conf_name = None
        for conf, venue_ids in conferences.items():
            if venue_id in venue_ids:
                conf_name = conf
                break

        if conf_name not in results:
            results[conf_name] = []

        results[conf_name].append(result)

        if result["status"] == "active":
            active_venues.append(venue_id)
            print(f"  [OK] Active - {result['papers_count']} papers, sample venue: {result['sample_venue']}")
        else:
            print(f"  [FAIL] {result['status']}")

        # Add delay to avoid rate limiting
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for conf_name, venue_results in results.items():
        active_count = sum(1 for r in venue_results if r["status"] == "active")
        print(f"\n{conf_name}: {active_count}/{len(venue_results)} active venues")
        for result in venue_results:
            if result["status"] == "active":
                year = result["venue_id"].split("/")[1]
                print(f"  {year}: {result['papers_count']}+ papers ({result['sample_venue']})")

    print(f"\nTotal active venues: {len(active_venues)}")
    return results

if __name__ == "__main__":
    results = discover_conferences()