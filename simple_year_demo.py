#!/usr/bin/env python3
"""
Simple demo showing free year input works
"""

from multi_conference_crawler import MultiConferenceCrawler

def main():
    print("Simple Free Year Input Demo")
    print("=" * 40)

    crawler = MultiConferenceCrawler()

    # Test with different years
    test_cases = [
        ("NeurIPS", 2025),
        ("NeurIPS", 2024),
        ("NeurIPS", 2023),
    ]

    for conference, year in test_cases:
        print(f"\nTesting {conference} {year}...")

        try:
            # Just test API accessibility with a small limit
            venue_id = f"{conference}.cc/{year}/Conference"
            if conference == "NeurIPS":
                venue_id = f"NeurIPS.cc/{year}/Conference"

            data = crawler.fetch_all_papers(venue_id, limit=1)
            notes = data.get("notes", [])

            if notes:
                print(f"  [OK] {year} is accessible")
                sample_venue = notes[0].get("content", {}).get("venue", {}).get("value", "")
                print(f"       Sample venue: {sample_venue}")
            else:
                print(f"  [NO DATA] {year} has no accessible papers")

        except Exception as e:
            print(f"  [ERROR] {year}: {e}")

    print(f"\nDemo completed!")
    print("You can now use any year when running the crawler.")
    print("Example: python multi_conference_crawler.py")
    print("Then select conference and enter any year like 2024, 2023, 2022, etc.")

if __name__ == "__main__":
    main()