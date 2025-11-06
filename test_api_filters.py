#!/usr/bin/env python3
"""
Test different API filter parameters to see if we can filter by decision directly
"""

import requests
import json

def test_venue_filter():
    """Test if we can filter by venue content directly"""

    # Test different filter approaches
    test_cases = [
        {
            "name": "Direct venue filter",
            "params": {
                "content.venueid": "NeurIPS.cc/2025/Conference",
                "content.venue": "NeurIPS 2025 oral",
                "limit": 5
            }
        },
        {
            "name": "Venue contains oral",
            "params": {
                "content.venueid": "NeurIPS.cc/2025/Conference",
                "content.venue": "oral",
                "limit": 5
            }
        },
        {
            "name": "Filter by forum (for oral papers)",
            "params": {
                "forum": "KurYdcCbjv",  # Known oral paper ID from previous test
                "limit": 5
            }
        }
    ]

    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Parameters: {test_case['params']}")

        try:
            response = requests.get(
                "https://api2.openreview.net/notes",
                params=test_case['params'],
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()
            data = response.json()
            notes = data.get("notes", [])

            print(f"Results: {len(notes)} papers found")
            for note in notes[:2]:  # Show first 2 results
                venue = note.get("content", {}).get("venue", {}).get("value", "")
                title = note.get("content", {}).get("title", {}).get("value", "")
                print(f"  Venue: {venue}")
                print(f"  Title: {title[:50]}...")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_venue_filter()