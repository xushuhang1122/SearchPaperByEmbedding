#!/usr/bin/env python3
"""
Test the free year input functionality
"""

import os
import json
from multi_conference_crawler import MultiConferenceCrawler

def test_various_years():
    """Test crawling different years for NeurIPS"""
    print("Testing free year input functionality...")
    print("=" * 60)

    crawler = MultiConferenceCrawler()

    # Test different years
    test_years = [2025, 2024, 2023, 2022, 2021]

    results = {}

    for year in test_years:
        print(f"\nTesting NeurIPS {year}...")

        try:
            papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
                conference="NeurIPS",
                year=year,
                output_dir="test_free_year"
            )

            results[f"neurips_{year}"] = {
                "total": len(all_papers),
                "by_decision": {k: len(v) for k, v in papers_by_decision.items()},
                "status": "success"
            }

            print(f"  Success: {len(all_papers)} papers found")
            for decision, count in {k: len(v) for k, v in papers_by_decision.items()}.items():
                print(f"    {decision}: {count} papers")

        except Exception as e:
            print(f"  Failed: {e}")
            results[f"neurips_{year}"] = {
                "total": 0,
                "by_decision": {},
                "status": f"error: {str(e)}"
            }

    # Save results
    with open("test_free_year/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to test_free_year/results.json")
    return results

def test_edge_cases():
    """Test edge cases for year input"""
    print("\nTesting edge cases...")
    print("=" * 60)

    crawler = MultiConferenceCrawler()

    # Test edge cases
    edge_cases = [
        ("NeurIPS", 2020),  # Older year
        ("ICML", 2025),     # Future year
        ("ICLR", 2022),     # Older ICLR
    ]

    for conference, year in edge_cases:
        print(f"\nTesting {conference} {year}...")

        try:
            # Just test API accessibility, not full crawl
            venue_id = f"{conference.lower()}.cc/{year}/Conference"
            if conference == "ICLR":
                venue_id = f"ICLR.cc/{year}/Conference"
            elif conference == "ICML":
                venue_id = f"ICML.cc/{year}/Conference"

            # Test basic API call
            data = crawler.fetch_all_papers(venue_id, limit=2)
            notes = data.get("notes", [])

            print(f"  API accessible: {len(notes)} papers found")
            if notes:
                sample_venue = notes[0].get("content", {}).get("venue", {}).get("value", "")
                print(f"  Sample venue: {sample_venue}")

        except Exception as e:
            print(f"  API error: {e}")

def main():
    """Main test function"""
    print("Free Year Input Test Suite")
    print("=" * 60)

    # Create output directory
    os.makedirs("test_free_year", exist_ok=True)

    # Test various years
    test_various_years()

    # Test edge cases
    test_edge_cases()

    print("\nTest completed!")
    print("Check the test_free_year directory for results.")

if __name__ == "__main__":
    main()