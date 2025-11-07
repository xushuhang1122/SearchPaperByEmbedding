#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to filter and sort papers by decision type and similarity score.
按decision类型筛选论文并按similarity排序的脚本。
"""

import json
import argparse
from typing import Dict, List, Any


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file '{file_path}': {e}")
        return {}


def group_papers_by_decision(data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Group papers by their decision type and sort by similarity (descending)."""
    decision_groups = {}

    for result in data.get('results', []):
        decision = result['paper']['decision']
        if decision not in decision_groups:
            decision_groups[decision] = []
        decision_groups[decision].append(result)

    # Sort each group by similarity (descending)
    for decision in decision_groups:
        decision_groups[decision].sort(key=lambda x: x['similarity'], reverse=True)

    return decision_groups


def print_paper_summary(paper_data: Dict[str, Any], rank: int) -> None:
    """Print a summary of a paper."""
    paper = paper_data['paper']
    similarity = paper_data['similarity']

    print(f"{rank}. {paper['title']}")
    print(f"   Similarity: {similarity:.4f}")
    print(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
    print(f"   Venue: {paper['venue']}")
    print(f"   URL: {paper['forum_url']}")
    print()


def save_filtered_results(decision_groups: Dict[str, List[Dict[str, Any]]],
                         output_file: str) -> None:
    """Save filtered results to a JSON file."""
    output_data = {
        'model': decision_groups[next(iter(decision_groups))][0]['paper'].get('_source_file', '').split('_')[0].upper() if decision_groups else '',
        'total_papers': sum(len(papers) for papers in decision_groups.values()),
        'decision_counts': {decision: len(papers) for decision, papers in decision_groups.items()},
        'results_by_decision': {}
    }

    for decision, papers in decision_groups.items():
        output_data['results_by_decision'][decision] = {
            'count': len(papers),
            'papers': papers
        }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Filtered results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Filter and sort papers by decision type')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('-o', '--output', default='filtered_papers.json',
                       help='Output JSON file path (default: filtered_papers.json)')
    parser.add_argument('-d', '--decision', type=str,
                       help='Filter by specific decision type (oral, poster, spotlight)')
    parser.add_argument('--top', type=int,
                       help='Show top N papers from each decision type')
    parser.add_argument('--list-decisions', action='store_true',
                       help='List all available decision types and exit')

    args = parser.parse_args()

    # Load input data
    data = load_json_file(args.input_file)
    if not data:
        return

    # Group papers by decision
    decision_groups = group_papers_by_decision(data)

    # List decision types if requested
    if args.list_decisions:
        print("Available decision types:")
        for decision in sorted(decision_groups.keys()):
            count = len(decision_groups[decision])
            print(f"  {decision}: {count} papers")
        return

    # Filter by specific decision if requested
    if args.decision:
        if args.decision not in decision_groups:
            print(f"Error: Decision type '{args.decision}' not found.")
            print(f"Available types: {sorted(decision_groups.keys())}")
            return
        decision_groups = {args.decision: decision_groups[args.decision]}

    # Display results
    print(f"Found {data.get('total', 0)} total papers\n")

    for decision in sorted(decision_groups.keys()):
        papers = decision_groups[decision]
        if args.top:
            papers = papers[:args.top]
            print(f"=== {decision.upper()} (Top {args.top}) ===")
        else:
            print(f"=== {decision.upper()} ({len(papers)} papers) ===")

        for i, paper_data in enumerate(papers, 1):
            print_paper_summary(paper_data, i)

    # Save results
    save_filtered_results(decision_groups, args.output)


if __name__ == '__main__':
    main()