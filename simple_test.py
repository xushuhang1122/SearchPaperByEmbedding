#!/usr/bin/env python3
"""
Simple test to verify the separate crawling works for one decision type
"""

import os
import json
import time
from crawl import crawl_papers_by_decision_custom

def test_single_decision():
    """Test crawling only poster papers to avoid rate limiting"""
    print("Testing separate crawling for poster papers only...")

    output_dir = "simple_test_output"

    # Define only poster pattern to avoid rate limiting
    single_pattern = {
        "poster": "NeurIPS 2025 poster"
    }

    try:
        papers_by_decision, all_papers = crawl_papers_by_decision_custom(
            venue_id="NeurIPS.cc/2025/Conference",
            decision_patterns=single_pattern,
            output_dir=output_dir,
            limit=20  # Very small limit for testing
        )

        print(f"Successfully crawled {len(all_papers)} poster papers")

        # Verify the data structure
        poster_file = os.path.join(output_dir, "poster_papers.json")
        if os.path.exists(poster_file):
            with open(poster_file, 'r', encoding='utf-8') as f:
                papers = json.load(f)
            print(f"Poster papers saved: {len(papers)}")

            # Check first paper
            if papers:
                first_paper = papers[0]
                print(f"Sample paper title: {first_paper['title'][:60]}...")
                print(f"Decision: {first_paper['decision']}")
                print(f"Venue: {first_paper['venue']}")
                print(f"Authors: {len(first_paper['authors'])} authors")
                print(f"Abstract length: {len(first_paper['abstract'])} characters")
                print("Data structure looks correct!")
                return True
            else:
                print("No papers found in the file")
                return False
        else:
            print(f"File {poster_file} was not created")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_single_decision()
    if success:
        print("\nSimple test passed!")
    else:
        print("\nSimple test failed!")