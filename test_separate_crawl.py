#!/usr/bin/env python3
"""
Test the new separate crawling by decision type functionality
"""

import os
import json
import time
from crawl import crawl_papers_by_decision, crawl_papers_by_decision_custom

def test_separate_crawl():
    """Test the new separate crawling functionality"""
    print("Testing separate crawling by decision type...")

    output_dir = "test_separate_crawl"

    # Test the main function
    print("\n=== Testing main crawl_papers_by_decision function ===")
    try:
        papers_by_decision, all_papers = crawl_papers_by_decision(
            venue_id="NeurIPS.cc/2025/Conference",
            output_dir=output_dir
        )

        print(f"Successfully crawled {len(all_papers)} total papers")

        # Check files were created
        expected_files = [
            "neurips2025_oral.json",
            "neurips2025_spotlight.json",
            "neurips2025_poster.json",
            "neurips2025_all.json"
        ]

        for filename in expected_files:
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                print(f"  [OK] {filename}: {len(papers)} papers")
            else:
                print(f"  [MISSING] {filename}: Not created")

        return True

    except Exception as e:
        print(f"Error in main function: {e}")
        return False

def test_custom_patterns():
    """Test custom decision patterns functionality"""
    print("\n=== Testing custom patterns function ===")

    custom_output_dir = "test_custom_crawl"

    # Define custom patterns (test only oral and poster)
    custom_patterns = {
        "oral_presentations": "NeurIPS 2025 oral",
        "poster_presentations": "NeurIPS 2025 poster"
    }

    try:
        papers_by_decision, all_papers = crawl_papers_by_decision_custom(
            venue_id="NeurIPS.cc/2025/Conference",
            decision_patterns=custom_patterns,
            output_dir=custom_output_dir,
            limit=50  # Small limit for testing
        )

        print(f"Successfully crawled {len(all_papers)} total papers with custom patterns")

        # Check custom files were created
        for decision_name in custom_patterns.keys():
            filename = f"{decision_name.lower()}_papers.json"
            filepath = os.path.join(custom_output_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                print(f"  [OK] {filename}: {len(papers)} papers")
            else:
                print(f"  [MISSING] {filename}: Not created")

        return True

    except Exception as e:
        print(f"Error in custom function: {e}")
        return False

def verify_data_structure(papers_file):
    """Verify the data structure of crawled papers"""
    print(f"\n=== Verifying data structure for {papers_file} ===")

    if not os.path.exists(papers_file):
        print(f"File {papers_file} does not exist")
        return False

    with open(papers_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    if not papers:
        print("No papers found")
        return False

    # Check first paper structure
    first_paper = papers[0]
    required_fields = ["id", "title", "authors", "abstract", "decision", "venue", "forum_url"]

    missing_fields = [field for field in required_fields if field not in first_paper]

    if missing_fields:
        print(f"Missing required fields: {missing_fields}")
        return False

    print(f"[OK] Data structure is valid")
    print(f"  Sample paper: {first_paper['title'][:50]}...")
    print(f"  Decision: {first_paper['decision']}")
    print(f"  Venue: {first_paper['venue']}")

    return True

if __name__ == "__main__":
    print("Testing separate crawling functionality...")
    print("=" * 60)

    # Test main function
    success1 = test_separate_crawl()

    # Test custom patterns
    success2 = test_custom_patterns()

    # Verify data structure
    if success1:
        verify_data_structure("test_separate_crawl/neurips2025_oral.json")
        verify_data_structure("test_separate_crawl/neurips2025_all.json")

    if success1 and success2:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")