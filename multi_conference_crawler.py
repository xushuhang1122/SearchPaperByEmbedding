#!/usr/bin/env python3
"""
Multi-conference paper crawler with decision categorization
Supports multiple CCF-A conferences across different years
"""

import requests
import json
import time
import os
from collections import defaultdict

class ConferenceConfig:
    """Configuration for different conferences and their API patterns"""

    # Conference configurations based on API testing results
    CONFERENCES = {
        "NeurIPS": {
            "name": "NeurIPS",
            "years": [2025, 2024, 2023],
            "venue_pattern": "NeurIPS.cc/{year}/Conference",
            "decision_patterns": {
                "oral": "NeurIPS {year} oral",
                "spotlight": "NeurIPS {year} spotlight",
                "poster": "NeurIPS {year} poster"
            }
        },
        "ICML": {
            "name": "ICML",
            "years": [2024, 2023],
            "venue_pattern": "ICML.cc/{year}/Conference",
            "decision_patterns": {
                # ICML uses different pattern format, will use general approach
                "all": ""  # Will fetch all papers and categorize locally
            }
        },
        "ICLR": {
            "name": "ICLR",
            "years": [2024, 2023],
            "venue_pattern": "ICLR.cc/{year}/Conference",
            "decision_patterns": {
                # ICLR uses different pattern format, will use general approach
                "all": ""  # Will fetch all papers and categorize locally
            }
        }
    }

class MultiConferenceCrawler:
    """Multi-conference paper crawler"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def fetch_papers_by_decision(self, venue_id, venue_pattern, offset=0, limit=1000):
        """Fetch papers with specific venue pattern (decision type)"""
        url = "https://api2.openreview.net/notes"
        params = {
            "content.venueid": venue_id,
            "content.venue": venue_pattern,
            "details": "replyCount,invitation",
            "limit": limit,
            "offset": offset,
            "sort": "number:desc"
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_all_papers(self, venue_id, offset=0, limit=1000):
        """Fetch all papers from a venue"""
        url = "https://api2.openreview.net/notes"
        params = {
            "content.venueid": venue_id,
            "details": "replyCount,invitation",
            "limit": limit,
            "offset": offset,
            "sort": "number:desc"
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def detect_decision_from_venue(self, venue_string):
        """Detect decision type from venue string"""
        venue_lower = venue_string.lower()

        if "oral" in venue_lower:
            return "oral"
        elif "spotlight" in venue_lower:
            return "spotlight"
        elif "poster" in venue_lower:
            return "poster"
        elif "accept" in venue_lower and "reject" not in venue_lower:
            return "accepted"
        elif "reject" in venue_lower:
            return "reject"
        else:
            return "unknown"

    def crawl_conference_by_decision(self, conference, year, output_dir):
        """Crawl papers for a specific conference and year by decision type"""
        config = ConferenceConfig.CONFERENCES[conference]
        venue_id = config["venue_pattern"].format(year=year)

        print(f"\nCrawling {conference} {year}...")
        print(f"Venue ID: {venue_id}")

        # Create conference/year specific output directory
        conf_output_dir = os.path.join(output_dir, f"{conference.lower()}_{year}")
        os.makedirs(conf_output_dir, exist_ok=True)

        papers_by_decision = {}
        all_papers = []

        decision_patterns = {
            key: pattern.format(year=year) if pattern else ""
            for key, pattern in config["decision_patterns"].items()
        }

        # Check if we have specific decision patterns or need general approach
        has_specific_patterns = any(decision_patterns.values()) and "all" not in decision_patterns

        if has_specific_patterns:
            # Use specific decision patterns (like NeurIPS)
            for decision, venue_pattern in decision_patterns.items():
                if not venue_pattern:
                    continue

                print(f"  Fetching {decision} papers...")
                decision_papers = []
                offset = 0

                while True:
                    try:
                        data = self.fetch_papers_by_decision(venue_id, venue_pattern, offset, 1000)
                        notes = data.get("notes", [])

                        if not notes:
                            break

                        for note in notes:
                            paper = self.extract_paper_info(note, venue_pattern, decision)
                            decision_papers.append(paper)
                            all_papers.append(paper)

                        print(f"    Fetched {len(notes)} {decision} papers (total: {len(decision_papers)})")

                        if len(notes) < 1000:
                            break

                        offset += 1000
                        time.sleep(1.0)  # Rate limiting

                    except Exception as e:
                        print(f"    Error fetching {decision} papers: {e}")
                        break

                papers_by_decision[decision] = decision_papers

                # Save immediately
                self.save_decision_papers(decision_papers, decision, conf_output_dir, conference, year)

        else:
            # Use general approach - fetch all papers and categorize locally
            print("  Using general approach - fetching all papers and categorizing locally...")
            offset = 0

            while True:
                try:
                    data = self.fetch_all_papers(venue_id, offset, 1000)
                    notes = data.get("notes", [])

                    if not notes:
                        break

                    for note in notes:
                        venue_field = note.get("content", {}).get("venue", {}).get("value", "")
                        detected_decision = self.detect_decision_from_venue(venue_field)

                        paper = self.extract_paper_info(note, venue_field, detected_decision)
                        all_papers.append(paper)

                        if detected_decision not in papers_by_decision:
                            papers_by_decision[detected_decision] = []
                        papers_by_decision[detected_decision].append(paper)

                    print(f"    Fetched {len(notes)} papers (total: {len(all_papers)})")

                    if len(notes) < 1000:
                        break

                    offset += 1000
                    time.sleep(1.0)

                except Exception as e:
                    print(f"    Error fetching papers: {e}")
                    break

            # Save all categories
            for decision, decision_papers in papers_by_decision.items():
                self.save_decision_papers(decision_papers, decision, conf_output_dir, conference, year)

        # Save combined file
        combined_file = os.path.join(conf_output_dir, f"{conference.lower()}_{year}_all.json")
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(all_papers, f, ensure_ascii=False, indent=2)

        print(f"\nSummary for {conference} {year}:")
        total_papers = 0
        for decision, papers in papers_by_decision.items():
            print(f"  {decision}: {len(papers)} papers")
            total_papers += len(papers)
        print(f"Total: {total_papers} papers")

        return papers_by_decision, all_papers

    def extract_paper_info(self, note, venue, decision):
        """Extract standardized paper information"""
        return {
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

    def save_decision_papers(self, papers, decision, output_dir, conference, year):
        """Save papers for a specific decision type"""
        filename = f"{conference.lower()}_{year}_{decision}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)

        print(f"    Saved {len(papers)} {decision} papers to {filepath}")

def select_conference():
    """Interactive conference selection"""
    print("\n" + "="*60)
    print("SELECT CONFERENCE")
    print("="*60)

    conferences = list(ConferenceConfig.CONFERENCES.keys())

    for i, conf in enumerate(conferences, 1):
        config = ConferenceConfig.CONFERENCES[conf]
        years = config["years"]
        print(f"{i}. {conf} (any year, commonly {years[0]}-{years[-1]})")

    while True:
        try:
            choice = input(f"\nSelect conference (1-{len(conferences)}): ").strip()
            index = int(choice) - 1
            if 0 <= index < len(conferences):
                return conferences[index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def select_year(conference):
    """Interactive year selection for a conference"""
    config = ConferenceConfig.CONFERENCES[conference]

    print(f"\nEnter year for {conference}")
    print(f"Common years: {config['years']}")
    print("You can enter any year (e.g., 2025, 2024, 2023, 2022, etc.)")

    while True:
        year_input = input(f"\nEnter year (e.g., 2024): ").strip()

        # Validate year input
        try:
            year = int(year_input)
            if year < 2000 or year > 2030:
                print("Please enter a reasonable year between 2000 and 2030.")
                continue
            return year
        except ValueError:
            print("Please enter a valid year number.")

def main():
    """Main function with interactive selection"""
    print("="*60)
    print("MULTI-CONFERENCE PAPER CRAWLER")
    print("="*60)

    crawler = MultiConferenceCrawler()

    while True:
        # Select conference
        conference = select_conference()

        # Select year
        year = select_year(conference)

        # Select output directory
        default_output = "crawled_papers"
        output_dir = input(f"\nOutput directory (default: {default_output}): ").strip()
        if not output_dir:
            output_dir = default_output

        # Crawl the selected conference
        try:
            papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
                conference, year, output_dir
            )

            print(f"\nSuccessfully crawled {len(all_papers)} papers from {conference} {year}!")
            print(f"Files saved to: {os.path.join(output_dir, f'{conference.lower()}_{year}')}")

        except Exception as e:
            print(f"\nError crawling {conference} {year}: {e}")

        # Ask if user wants to continue
        continue_choice = input("\nCrawl another conference? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

    print("\nThank you for using the Multi-Conference Paper Crawler!")

if __name__ == "__main__":
    main()