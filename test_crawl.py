#!/usr/bin/env python3
"""
Test script for the enhanced crawler with decision categorization
"""

import os
import json
from crawl import crawl_papers_by_decision

def test_neurips_crawler():
    """Test the NeurIPS 2025 crawler with decision categorization"""
    print("Testing NeurIPS 2025 crawler with decision categorization...")

    # Test with a small limit to avoid too many API calls
    output_dir = "test_neurips2025_papers"

    try:
        papers_by_decision, all_papers = crawl_papers_by_decision(
            venue_id="NeurIPS.cc/2025/Conference",
            output_dir=output_dir
        )

        print(f"\nTest completed successfully!")
        print(f"Total papers crawled: {len(all_papers)}")

        # Check if files were created
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
                print(f"  {filename}: {len(papers)} papers")
            else:
                print(f"  {filename}: Not created")

        return True

    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_neurips_crawler()
    if success:
        print("\nTest passed!")
    else:
        print("\nTest failed!")