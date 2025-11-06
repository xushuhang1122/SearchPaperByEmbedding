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

def fetch_papers_by_decision(venue_id, venue_pattern, offset=0, limit=1000):
    """
    Fetch papers from OpenReview API with specific venue pattern (decision type)

    Args:
        venue_id: The venue ID (e.g., "NeurIPS.cc/2025/Conference")
        venue_pattern: Exact venue pattern to filter (e.g., "NeurIPS 2025 oral")
        offset: Pagination offset
        limit: Number of papers per request

    Returns:
        List of papers with the specified venue pattern
    """
    url = "https://api2.openreview.net/notes"
    params = {
        "content.venueid": venue_id,
        "content.venue": venue_pattern,  # Exact match for decision type
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
    Crawl papers from OpenReview by decision type with separate API calls

    Args:
        venue_id: The venue ID (e.g., "NeurIPS.cc/2025/Conference")
        output_dir: Directory to save categorized JSON files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define decision types and their exact venue patterns for NeurIPS 2025
    decision_patterns = {
        "oral": "NeurIPS 2025 oral",
        "spotlight": "NeurIPS 2025 spotlight",
        "poster": "NeurIPS 2025 poster",
        # Note: "NeurIPS 2025 reject" pattern might not exist publicly
        # We'll handle rejects differently if needed
    }

    papers_by_decision = {}
    all_papers = []

    print(f"Crawling papers from {venue_id} by decision type...")

    for decision, venue_pattern in decision_patterns.items():
        print(f"\nFetching {decision} papers...")

        decision_papers = []
        offset = 0
        limit = 1000

        while True:
            try:
                data = fetch_papers_by_decision(venue_id, venue_pattern, offset, limit)
                notes = data.get("notes", [])

                if not notes:
                    break

                # Process papers for this decision type
                for note in notes:
                    paper = {
                        "id": note.get("id"),
                        "number": note.get("number"),
                        "title": note.get("content", {}).get("title", {}).get("value", ""),
                        "authors": note.get("content", {}).get("authors", {}).get("value", []),
                        "abstract": note.get("content", {}).get("abstract", {}).get("value", ""),
                        "keywords": note.get("content", {}).get("keywords", {}).get("value", []),
                        "primary_area": note.get("content", {}).get("primary_area", {}).get("value", ""),
                        "venue": venue_pattern,
                        "decision": decision,
                        "forum_url": f"https://openreview.net/forum?id={note.get('id')}"
                    }
                    decision_papers.append(paper)
                    all_papers.append(paper)

                print(f"  Fetched {len(notes)} {decision} papers (total: {len(decision_papers)})")

                if len(notes) < limit:
                    break

                offset += limit
                time.sleep(1.0)  # Increased rate limiting to avoid 429 errors

            except Exception as e:
                print(f"  Error fetching {decision} papers: {e}")
                break

        papers_by_decision[decision] = decision_papers

        # Save papers for this decision type immediately
        output_file = os.path.join(output_dir, f"neurips2025_{decision}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(decision_papers, f, ensure_ascii=False, indent=2)
        print(f"  Saved {len(decision_papers)} {decision} papers to {output_file}")

    # Save combined file with all accepted papers
    combined_file = os.path.join(output_dir, "neurips2025_all.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    print(f"\nSummary:")
    total_accepted = 0
    for decision, papers in papers_by_decision.items():
        print(f"  {decision}: {len(papers)} papers")
        total_accepted += len(papers)
    print(f"Total accepted papers: {total_accepted}")
    print(f"Files saved to {output_dir}")

    return papers_by_decision, all_papers

def crawl_papers_by_decision_custom(venue_id, decision_patterns, output_dir, limit=1000):
    """
    Crawl papers from OpenReview by custom decision patterns

    Args:
        venue_id: The venue ID (e.g., "NeurIPS.cc/2025/Conference")
        decision_patterns: Dictionary mapping decision names to venue patterns
                          e.g., {"oral": "NeurIPS 2025 oral", "poster": "NeurIPS 2025 poster"}
        output_dir: Directory to save categorized JSON files
        limit: Number of papers per API request

    Returns:
        Tuple of (papers_by_decision, all_papers)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    papers_by_decision = {}
    all_papers = []

    print(f"Crawling papers from {venue_id} with custom decision patterns...")

    for decision, venue_pattern in decision_patterns.items():
        print(f"\nFetching {decision} papers (pattern: '{venue_pattern}')...")

        decision_papers = []
        offset = 0

        while True:
            try:
                data = fetch_papers_by_decision(venue_id, venue_pattern, offset, limit)
                notes = data.get("notes", [])

                if not notes:
                    break

                # Process papers for this decision type
                for note in notes:
                    paper = {
                        "id": note.get("id"),
                        "number": note.get("number"),
                        "title": note.get("content", {}).get("title", {}).get("value", ""),
                        "authors": note.get("content", {}).get("authors", {}).get("value", []),
                        "abstract": note.get("content", {}).get("abstract", {}).get("value", ""),
                        "keywords": note.get("content", {}).get("keywords", {}).get("value", []),
                        "primary_area": note.get("content", {}).get("primary_area", {}).get("value", ""),
                        "venue": venue_pattern,
                        "decision": decision,
                        "forum_url": f"https://openreview.net/forum?id={note.get('id')}"
                    }
                    decision_papers.append(paper)
                    all_papers.append(paper)

                print(f"  Fetched {len(notes)} {decision} papers (total: {len(decision_papers)})")

                if len(notes) < limit:
                    break

                offset += limit
                time.sleep(1.0)  # Increased rate limiting to avoid 429 errors

            except Exception as e:
                print(f"  Error fetching {decision} papers: {e}")
                break

        papers_by_decision[decision] = decision_papers

        # Save papers for this decision type immediately
        output_file = os.path.join(output_dir, f"{decision.lower()}_papers.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(decision_papers, f, ensure_ascii=False, indent=2)
        print(f"  Saved {len(decision_papers)} {decision} papers to {output_file}")

    # Save combined file with all papers
    combined_file = os.path.join(output_dir, "all_papers.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    print(f"\nSummary:")
    for decision, papers in papers_by_decision.items():
        print(f"  {decision}: {len(papers)} papers")
    print(f"Total papers: {len(all_papers)}")
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

