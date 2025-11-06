#!/usr/bin/env python3
"""
Demo script showing how to use the multi-conference crawler programmatically
"""

import os
import json
from multi_conference_crawler import MultiConferenceCrawler

def demo_crawl_neurips_2024():
    """Demo: Crawl NeurIPS 2024 papers"""
    print("Demo: Crawling NeurIPS 2024 papers...")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    try:
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="NeurIPS",
            year=2024,
            output_dir="demo_output"
        )

        print(f"\nDemo completed successfully!")
        print(f"Total papers: {len(all_papers)}")

        for decision, papers in papers_by_decision.items():
            print(f"  {decision}: {len(papers)} papers")

        return True

    except Exception as e:
        print(f"Demo failed: {e}")
        return False

def demo_batch_crawl():
    """Demo: Crawl multiple conferences"""
    print("Demo: Batch crawling multiple conferences...")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    # Define conferences to crawl
    crawl_targets = [
        ("NeurIPS", 2025),
        ("NeurIPS", 2024),
        ("ICML", 2024),
        ("ICLR", 2024)
    ]

    results = {}

    for conference, year in crawl_targets:
        print(f"\nCrawling {conference} {year}...")

        try:
            papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
                conference=conference,
                year=year,
                output_dir="batch_demo_output"
            )

            results[f"{conference}_{year}"] = {
                "total": len(all_papers),
                "by_decision": {k: len(v) for k, v in papers_by_decision.items()}
            }

            print(f"  Success: {len(all_papers)} papers")

        except Exception as e:
            print(f"  Failed: {e}")
            results[f"{conference}_{year}"] = {"error": str(e)}

    # Save summary
    summary_file = "batch_demo_output/crawl_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nBatch crawl summary saved to {summary_file}")
    return results

def interactive_demo():
    """Interactive demo"""
    print("Interactive Multi-Conference Crawler Demo")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    while True:
        print("\nOptions:")
        print("1. Crawl NeurIPS 2024 (quick demo)")
        print("2. Crawl NeurIPS 2025")
        print("3. Crawl ICML 2024")
        print("4. Batch crawl all available")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_crawl_neurips_2024()
        elif choice == "2":
            try:
                crawler.crawl_conference_by_decision("NeurIPS", 2025, "demo_output")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                crawler.crawl_conference_by_decision("ICML", 2024, "demo_output")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "4":
            demo_batch_crawl()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Multi-Conference Crawler Demo")
    print("This demo shows how to use the crawler programmatically")
    print()

    demo_mode = input("Select demo mode:\n1. Quick demo (NeurIPS 2024)\n2. Batch demo (all conferences)\n3. Interactive demo\n\nChoice (1-3): ").strip()

    if demo_mode == "1":
        demo_crawl_neurips_2024()
    elif demo_mode == "2":
        demo_batch_crawl()
    elif demo_mode == "3":
        interactive_demo()
    else:
        print("Running quick demo by default...")
        demo_crawl_neurips_2024()