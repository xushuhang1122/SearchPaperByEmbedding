#!/usr/bin/env python3
"""
Small scale test of the enhanced crawler
"""

import os
import json
from crawl import crawl_papers_by_decision

# Create a modified version with a small limit for testing
def crawl_papers_small(venue_id, output_dir, max_papers=50):
    """
    Modified version with small limit for testing
    """
    all_papers = []
    offset = 0
    limit = 50  # Only fetch 50 papers for testing

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store papers by decision
    from collections import defaultdict
    papers_by_decision = defaultdict(list)

    print(f"Fetching up to {max_papers} papers from {venue_id}...")

    # Only do one iteration for testing
    import requests
    import time

    url = "https://api2.openreview.net/notes"
    params = {
        "content.venueid": venue_id,
        "details": "replyCount,invitation",
        "limit": limit,
        "offset": offset,
        "sort": "number:desc"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    notes = data.get("notes", [])

    if not notes:
        print("No papers found")
        return papers_by_decision, all_papers

    for note in notes[:max_papers]:  # Limit to max_papers
        # Extract decision from venue field
        venue = note.get("content", {}).get("venue", {}).get("value", "")

        # Determine decision type from venue string
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

        paper = {
            "id": note.get("id"),
            "number": note.get("number"),
            "title": note.get("content", {}).get("title", {}).get("value", ""),
            "authors": note.get("content", {}).get("authors", {}).get("value", []),
            "abstract": note.get("content", {}).get("abstract", {}).get("value", ""),
            "keywords": note.get("content", {}).get("keywords", {}).get("value", []),
            "primary_area": note.get("content", {}).get("primary_area", {}).get("value", ""),
            "venue": venue,
            "decision": decision,
            "forum_url": f"https://openreview.net/forum?id={note.get('id')}"
        }

        all_papers.append(paper)
        papers_by_decision[decision].append(paper)

    print(f"Fetched {len(notes)} papers (processed: {len(all_papers)})")

    # Save papers by decision to separate files
    for decision, papers in papers_by_decision.items():
        output_file = os.path.join(output_dir, f"test_neurips2025_{decision}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(papers)} {decision} papers to {output_file}")

    # Also save a combined file
    combined_file = os.path.join(output_dir, "test_neurips2025_all.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    print(f"\nSummary:")
    for decision, papers in papers_by_decision.items():
        print(f"  {decision}: {len(papers)} papers")
    print(f"Total: {len(all_papers)} papers")
    print(f"Files saved to {output_dir}")

    return papers_by_decision, all_papers

if __name__ == "__main__":
    papers_by_decision, all_papers = crawl_papers_small(
        venue_id="NeurIPS.cc/2025/Conference",
        output_dir="test_output",
        max_papers=30
    )