import requests
import json
import time
import os
from collections import defaultdict

def fetch_submissions(venue_id, offset=0, limit=1000):
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
    return response.json()

def crawl_papers_by_decision(venue_id, output_dir):
    """
    Crawl papers from OpenReview and categorize them by decision (acceptance type)

    Args:
        venue_id: The venue ID (e.g., "NeurIPS.cc/2025/Conference")
        output_dir: Directory to save categorized JSON files
    """
    all_papers = []
    offset = 0
    limit = 1000

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store papers by decision
    papers_by_decision = defaultdict(list)

    print(f"Fetching papers from {venue_id}...")

    while True:
        data = fetch_submissions(venue_id, offset, limit)
        notes = data.get("notes", [])

        if not notes:
            break

        for note in notes:
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
                # Generic acceptance, categorize as poster by default
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

        print(f"Fetched {len(notes)} papers (total: {len(all_papers)})")

        if len(notes) < limit:
            break

        offset += limit
        time.sleep(0.5)

    # Save papers by decision to separate files
    for decision, papers in papers_by_decision.items():
        output_file = os.path.join(output_dir, f"neurips2025_{decision}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(papers)} {decision} papers to {output_file}")

    # Also save a combined file with all papers
    combined_file = os.path.join(output_dir, "neurips2025_all.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    print(f"\nSummary:")
    for decision, papers in papers_by_decision.items():
        print(f"  {decision}: {len(papers)} papers")
    print(f"Total: {len(all_papers)} papers")
    print(f"Files saved to {output_dir}")

    return papers_by_decision, all_papers

def crawl_papers(venue_id, output_file):
    """
    Legacy function that maintains backward compatibility
    """
    papers_by_decision, all_papers = crawl_papers_by_decision(venue_id, os.path.dirname(output_file))

    # Save to the specified output file for backward compatibility
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    return all_papers

if __name__ == "__main__":
    # Example usage for NeurIPS 2025 with decision categorization
    crawl_papers_by_decision(
        venue_id="NeurIPS.cc/2025/Conference",
        output_dir="neurips2025_papers"
    )

    # Legacy usage (still works)
    # crawl_papers(
    #     venue_id="ICLR.cc/2026/Conference/Submission",
    #     output_file="iclr2026_papers.json"
    # )

