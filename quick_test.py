#!/usr/bin/env python3
"""
Quick test to verify API response structure and decision categorization
"""

import requests
import json

def test_api_response():
    """Test the API response to verify decision extraction works"""
    url = "https://api2.openreview.net/notes"
    params = {
        "content.venueid": "NeurIPS.cc/2025/Conference",
        "details": "replyCount,invitation",
        "limit": 10,  # Only get 10 papers for testing
        "offset": 0,
        "sort": "number:desc"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        notes = data.get("notes", [])
        print(f"Found {len(notes)} papers")

        decisions_found = set()
        for i, note in enumerate(notes[:5]):  # Check first 5 papers
            venue = note.get("content", {}).get("venue", {}).get("value", "")
            title = note.get("content", {}).get("title", {}).get("value", "")

            # Determine decision type
            decision = "unknown"
            if "oral" in venue.lower():
                decision = "oral"
            elif "spotlight" in venue.lower():
                decision = "spotlight"
            elif "poster" in venue.lower():
                decision = "poster"
            elif "reject" in venue.lower() or "rejected" in venue.lower():
                decision = "reject"
            elif "accept" in venue.lower():
                decision = "poster"

            decisions_found.add(decision)
            print(f"{i+1}. Decision: {decision}")
            print(f"   Venue: {venue}")
            print(f"   Title: {title[:80]}...")
            print()

        print(f"Decisions found: {decisions_found}")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_api_response()