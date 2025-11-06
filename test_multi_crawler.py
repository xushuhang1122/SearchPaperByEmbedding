#!/usr/bin/env python3
"""
Test the multi-conference crawler functionality
"""

import os
import json
import time
from multi_conference_crawler import MultiConferenceCrawler, ConferenceConfig

def test_conference_configs():
    """Test conference configurations"""
    print("Testing conference configurations...")
    print("=" * 50)

    for conf_name, config in ConferenceConfig.CONFERENCES.items():
        print(f"\n{conf_name}:")
        print(f"  Years: {config['years']}")
        print(f"  Venue pattern: {config['venue_pattern']}")
        print(f"  Decision patterns: {list(config['decision_patterns'].keys())}")

def test_single_conference():
    """Test crawling a single conference with small sample"""
    print("\nTesting single conference crawl (small sample)...")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    # Test NeurIPS 2024 with small limit
    try:
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="NeurIPS",
            year=2024,
            output_dir="test_multi_crawl"
        )

        print(f"\nTest completed successfully!")
        print(f"Total papers crawled: {len(all_papers)}")

        # Check if files were created
        expected_dir = "test_multi_crawl/neurips_2024"
        if os.path.exists(expected_dir):
            files = os.listdir(expected_dir)
            print(f"Files created in {expected_dir}:")
            for file in files:
                filepath = os.path.join(expected_dir, file)
                if os.path.isfile(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        papers = json.load(f)
                    print(f"  {file}: {len(papers)} papers")
        else:
            print(f"Directory {expected_dir} was not created")

        return True

    except Exception as e:
        print(f"Test failed: {e}")
        return False

def test_general_approach():
    """Test the general approach for conferences without specific patterns"""
    print("\nTesting general approach for ICML...")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    try:
        # Test with very small limit to avoid rate limiting
        papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
            conference="ICML",
            year=2024,
            output_dir="test_general_approach"
        )

        print(f"General approach test completed!")
        print(f"Total papers: {len(all_papers)}")
        print(f"Decisions found: {list(papers_by_decision.keys())}")

        return True

    except Exception as e:
        print(f"General approach test failed: {e}")
        return False

def test_decision_detection():
    """Test decision detection logic"""
    print("\nTesting decision detection logic...")
    print("=" * 50)

    crawler = MultiConferenceCrawler()

    test_cases = [
        ("NeurIPS 2024 oral", "oral"),
        ("NeurIPS 2024 spotlight", "spotlight"),
        ("NeurIPS 2024 poster", "poster"),
        ("ICML 2024 Poster", "poster"),
        ("ICML 2024 Oral", "oral"),
        ("ICML 2024 Accepted Paper", "accepted"),
        ("Rejected", "reject"),
        ("Unknown venue", "unknown")
    ]

    all_passed = True
    for venue_str, expected in test_cases:
        detected = crawler.detect_decision_from_venue(venue_str)
        passed = detected == expected
        status = "[OK]" if passed else "[FAIL]"
        print(f"  {status} '{venue_str}' -> {detected} (expected: {expected})")
        if not passed:
            all_passed = False

    return all_passed

def verify_data_structure():
    """Verify the data structure of crawled papers"""
    print("\nVerifying data structure...")
    print("=" * 50)

    test_file = "test_multi_crawl/neurips_2024/neurips_2024_oral.json"

    if not os.path.exists(test_file):
        print(f"Test file {test_file} does not exist")
        return False

    with open(test_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    if not papers:
        print("No papers found in test file")
        return False

    first_paper = papers[0]
    required_fields = [
        "id", "title", "authors", "abstract", "decision",
        "venue", "forum_url", "keywords", "primary_area"
    ]

    missing_fields = [field for field in required_fields if field not in first_paper]

    if missing_fields:
        print(f"Missing required fields: {missing_fields}")
        return False

    print("[OK] Data structure is valid")
    print(f"  Sample paper: {first_paper['title'][:60]}...")
    print(f"  Decision: {first_paper['decision']}")
    print(f"  Venue: {first_paper['venue']}")
    print(f"  Authors: {len(first_paper['authors'])} authors")
    print(f"  Abstract length: {len(first_paper['abstract'])} characters")

    return True

def main():
    """Run all tests"""
    print("Multi-Conference Crawler Test Suite")
    print("=" * 60)

    results = []

    # Test 1: Conference configurations
    try:
        test_conference_configs()
        results.append(("Conference Configurations", True))
    except Exception as e:
        print(f"Conference config test failed: {e}")
        results.append(("Conference Configurations", False))

    # Test 2: Decision detection
    decision_test_passed = test_decision_detection()
    results.append(("Decision Detection", decision_test_passed))

    # Test 3: Single conference crawl (this might take time)
    print("\nNote: Single conference test may take a few minutes...")
    single_test_passed = test_single_conference()
    results.append(("Single Conference Crawl", single_test_passed))

    # Test 4: General approach
    print("\nNote: General approach test may take a few minutes...")
    general_test_passed = test_general_approach()
    results.append(("General Approach", general_test_passed))

    # Test 5: Data structure verification
    if single_test_passed:
        structure_test_passed = verify_data_structure()
        results.append(("Data Structure", structure_test_passed))
    else:
        results.append(("Data Structure", False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{total} tests")

    if passed == total:
        print("All tests passed! The multi-conference crawler is ready to use.")
    else:
        print("Some tests failed. Please check the issues above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)