#!/usr/bin/env python3
"""
Quick test for free year input functionality
"""

import os
from multi_conference_crawler import MultiConferenceCrawler

def quick_year_test():
    """Quick test with a few years"""
    print("Quick test: NeurIPS different years")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    # Test just a couple of years to avoid rate limiting
    test_years = [2024, 2023]

    for year in test_years:
        print(f"\nTesting NeurIPS {year}...")

        try:
            # Test API accessibility first
            venue_id = f"NeurIPS.cc/{year}/Conference"
            data = crawler.fetch_all_papers(venue_id, limit=2)
            notes = data.get("notes", [])

            if notes:
                print(f"  [OK] API accessible for {year}: {len(notes)} papers found")
                sample_venue = notes[0].get("content", {}).get("venue", {}).get("value", "")
                print(f"  Sample venue: {sample_venue}")

                # Now test actual crawling with small limit
                papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
                    conference="NeurIPS",
                    year=year,
                    output_dir="quick_year_test"
                )

                print(f"  [OK] Crawled {len(all_papers)} papers from {year}")
                for decision, papers in papers_by_decision.items():
                    print(f"    {decision}: {len(papers)} papers")

            else:
                print(f"  [NO DATA] No papers found for {year}")

        except Exception as e:
            print(f"  [ERROR] Failed for {year}: {e}")

if __name__ == "__main__":
    quick_year_test()