#!/usr/bin/env python3
"""
Demo script showing free year input functionality
"""

from multi_conference_crawler import MultiConferenceCrawler

def demo_programmatic_year_input():
    """Demo: Programmatic year input"""
    print("Demo: Programmatic year input")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    # Example 1: NeurIPS 2024
    print("\n1. Crawling NeurIPS 2024...")
    try:
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="NeurIPS",
            year=2024,
            output_dir="demo_year_output"
        )
        print(f"   Success: {len(all_papers)} papers")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 2: NeurIPS 2023
    print("\n2. Crawling NeurIPS 2023...")
    try:
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="NeurIPS",
            year=2023,
            output_dir="demo_year_output"
        )
        print(f"   Success: {len(all_papers)} papers")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 3: Test with different year
    print("\n3. Testing NeurIPS 2022...")
    try:
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="NeurIPS",
            year=2022,
            output_dir="demo_year_output"
        )
        print(f"   Success: {len(all_papers)} papers")
    except Exception as e:
        print(f"   Error: {e}")

def show_year_examples():
    """Show examples of year inputs"""
    print("\nYear Input Examples")
    print("=" * 50)

    examples = [
        ("NeurIPS", 2025, "Latest conference"),
        ("NeurIPS", 2024, "Recent conference"),
        ("NeurIPS", 2023, "Past conference"),
        ("NeurIPS", 2022, "Older conference"),
        ("ICML", 2024, "Different conference"),
        ("ICLR", 2024, "Different conference"),
    ]

    print("You can now use any year for supported conferences:")
    for conf, year, description in examples:
        print(f"  {conf} {year} - {description}")

    print("\nExample code:")
    print("  crawler.crawl_conference_by_decision('NeurIPS', 2025, 'output')")

def interactive_demo():
    """Interactive demo"""
    print("Interactive Free Year Input Demo")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. NeurIPS 2025")
        print("2. NeurIPS 2024")
        print("3. NeurIPS 2023")
        print("4. Custom year input")
        print("5. Show year examples")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        crawler = MultiConferenceCrawler()

        if choice == "1":
            try:
                crawler.crawl_conference_by_decision("NeurIPS", 2025, "demo_year_output")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "2":
            try:
                crawler.crawl_conference_by_decision("NeurIPS", 2024, "demo_year_output")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                crawler.crawl_conference_by_decision("NeurIPS", 2023, "demo_year_output")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "4":
            conference = input("Enter conference (NeurIPS/ICML/ICLR): ").strip()
            try:
                year = int(input("Enter year (e.g., 2024): ").strip())
                if 2000 <= year <= 2030:
                    crawler.crawl_conference_by_decision(conference, year, "demo_year_output")
                else:
                    print("Year must be between 2000 and 2030")
            except ValueError:
                print("Invalid input")
        elif choice == "5":
            show_year_examples()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Free Year Input Demo")
    print("This demo shows how you can now input any year for conferences")
    print()

    demo_mode = input("Select demo mode:\n1. Programmatic demo\n2. Interactive demo\n3. Show examples\n\nChoice (1-3): ").strip()

    if demo_mode == "1":
        demo_programmatic_year_input()
    elif demo_mode == "2":
        interactive_demo()
    elif demo_mode == "3":
        show_year_examples()
    else:
        print("Running programmatic demo by default...")
        demo_programmatic_year_input()