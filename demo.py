from search import PaperSearcher
import os
import json
import time

def find_all_json_files(directory):
    """Recursively find all JSON files in directory and subdirectories"""
    json_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                # Calculate relative path from crawled_papers directory
                rel_path = os.path.relpath(file_path, directory)
                json_files.append((file, file_path, rel_path))

    return json_files

def select_papers_files():
    """Let user select JSON files from crawled_papers directory and subdirectories"""
    crawled_dir = "crawled_papers"

    if not os.path.exists(crawled_dir):
        print(f"'{crawled_dir}' directory not found.")
        print("Please run the crawler first to generate papers data.")
        return None

    # Find all JSON files recursively
    json_files = find_all_json_files(crawled_dir)

    if not json_files:
        print(f"No JSON files found in '{crawled_dir}' directory and subdirectories.")
        return None

    # Group files by directory for better display
    dir_groups = {}
    for filename, filepath, rel_path in json_files:
        dir_name = os.path.dirname(rel_path)
        if dir_name not in dir_groups:
            dir_groups[dir_name] = []
        dir_groups[dir_name].append((filename, filepath, rel_path))

    # Display available files organized by directory
    print(f"\nFound {len(json_files)} JSON files in '{crawled_dir}' and subdirectories:")
    print("=" * 70)

    flat_list = []
    file_counter = 1

    # Sort directories for consistent display
    sorted_dirs = sorted(dir_groups.keys())

    for dir_name in sorted_dirs:
        if dir_name == '':
            display_name = f"{crawled_dir}/"
        else:
            display_name = f"{crawled_dir}/{dir_name}/"

        print(f"\n📁 {display_name}")
        print("-" * len(display_name))

        for filename, filepath, rel_path in sorted(dir_groups[dir_name]):
            # Get file size for better display
            file_size = os.path.getsize(filepath)
            size_mb = file_size / (1024 * 1024)

            # Show relative path for clarity
            if dir_name == '':
                display_filename = filename
            else:
                display_filename = f"{dir_name}/{filename}"

            print(f"  {file_counter:3d}. {display_filename:<50} ({size_mb:.1f} MB)")
            flat_list.append((file_counter, filename, filepath, rel_path))
            file_counter += 1

    selected_files = []

    while True:
        print(f"\n{'='*50}")
        print(f"Currently selected: {len(selected_files)} file(s)")

        if len(selected_files) > 0:
            print("\nSelected files:")
            for i, file_info in enumerate(selected_files, 1):
                # file_info is a tuple with 4 elements: (file_counter, filename, filepath, rel_path)
                if len(file_info) == 4:
                    _, filename, _, rel_path = file_info
                else:
                    # Fallback for older format
                    filename, filepath, rel_path = file_info

                if rel_path == filename:
                    print(f"  {i}. {filename}")
                else:
                    print(f"  {i}. {rel_path}")

        print("\nOptions:")
        print("Enter file number(s) to add (e.g., '1', '1,3,5', '1-5')")
        print("Enter 'done' to finish selection")
        print("Enter 'clear' to clear selection")
        print("Enter 'all' to select all files")

        choice = input("Your choice: ").strip()

        if choice.lower() == 'done':
            if len(selected_files) == 0:
                print("Please select at least one file.")
                continue
            break
        elif choice.lower() == 'clear':
            selected_files = []
            print("Selection cleared.")
            continue
        elif choice.lower() == 'all':
            selected_files = flat_list.copy()
            print(f"Selected all {len(json_files)} files.")
            continue
        else:
            # Handle different input formats: single number, comma-separated, or range
            numbers_to_add = []

            try:
                # Split by comma first
                parts = [part.strip() for part in choice.split(',')]

                for part in parts:
                    if '-' in part:  # Range format: "1-5"
                        start, end = map(int, part.split('-'))
                        numbers_to_add.extend(range(start, end + 1))
                    elif part.isdigit():  # Single number
                        numbers_to_add.append(int(part))

                # Add selected files
                added_count = 0
                for num in numbers_to_add:
                    file_index = num - 1  # Convert to 0-based index
                    if 0 <= file_index < len(flat_list):
                        file_info = flat_list[file_index]
                        if file_info not in selected_files:
                            selected_files.append(file_info)
                            display_name = file_info[3] if file_info[3] != file_info[1] else file_info[1]
                            print(f"Added: {display_name}")
                            added_count += 1
                        else:
                            display_name = file_info[3] if file_info[3] != file_info[1] else file_info[1]
                            print(f"Already selected: {display_name}")
                    else:
                        print(f"Invalid file number: {num}")

                if added_count == 0:
                    print("No new files added. Please check your input format.")

            except ValueError:
                print("Invalid input format. Please use numbers like '1', '1,3,5', or '1-5'.")

    return [file_info[2] for file_info in selected_files]  # filepath is at index 2

def merge_json_files(file_paths):
    """Merge multiple JSON files into one dataset"""
    all_papers = []
    source_files = []

    print("\nMerging JSON files...")
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        print(f"  Loading: {filename}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                papers = json.load(f)

            # Handle both single papers and lists
            if isinstance(papers, dict):
                papers = [papers]
            elif isinstance(papers, list):
                pass  # Already a list
            else:
                print(f"    Warning: Unexpected format in {filename}")
                continue

            # Add source file info to each paper
            for paper in papers:
                paper['_source_file'] = filename

            all_papers.extend(papers)
            source_files.append(filename)
            print(f"    Added {len(papers)} papers")

        except Exception as e:
            print(f"    Error loading {filename}: {e}")

    print(f"\nMerged {len(all_papers)} papers from {len(source_files)} files")
    print(f"Source files: {', '.join(source_files)}")

    return all_papers

def save_merged_dataset(papers, filename="merged_papers.json"):
    """Save merged dataset to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"\nMerged dataset saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving merged dataset: {e}")
        return None

def initialize_searcher():
    """Initialize the paper searcher with user-selected JSON files"""
    print("Paper Search Demo")
    print("=" * 40)
    print("First, let's select the papers dataset to search in.")

    # Let user select JSON files
    selected_files = select_papers_files()
    if not selected_files:
        return None

    # Merge the selected files
    merged_papers = merge_json_files(selected_files)
    if not merged_papers:
        print("No papers found in selected files.")
        return None

    # Ask if user wants to save merged dataset
    save_choice = input("\nSave merged dataset for future use? (y/n): ").strip().lower()
    if save_choice in ['y', 'yes']:
        timestamp = int(time.time())
        cache_dir = "cache"
        os.makedirs(cache_dir, exist_ok=True)
        merged_filename = os.path.join(cache_dir, f"merged_papers_{timestamp}.json")
        saved_file = save_merged_dataset(merged_papers, merged_filename)
        if saved_file:
            papers_file = saved_file
        else:
            papers_file = os.path.join(cache_dir, "temp_merged.json")
            save_merged_dataset(merged_papers, papers_file)
    else:
        papers_file = os.path.join(cache_dir, "temp_merged.json")
        save_merged_dataset(merged_papers, papers_file)

    # Initialize searcher with API embedding
    searcher = PaperSearcher(
        papers_file=papers_file,
        model_type='api',
        api_key=os.getenv('EMBEDDING_API_KEY')
    )

    print(f"\nInitializing search with {len(merged_papers)} papers...")
    print("Computing embeddings (this may take a while for large datasets)...")

    try:
        searcher.compute_embeddings()
        print("Embeddings computed successfully!")
        return searcher
    except Exception as e:
        print(f"Error computing embeddings: {e}")
        return None

def search_by_reference_papers(searcher):
    """Search using reference papers"""
    print("\n" + "="*60)
    print("SEARCH BY REFERENCE PAPERS")
    print("="*60)
    print("Enter title and abstract of reference papers (one at a time)")
    print("Enter empty title to finish adding papers\n")

    examples = []

    while True:
        title = input("Enter paper title (or press Enter to finish): ").strip()
        if not title:
            break

        abstract = input("Enter paper abstract (optional): ").strip()

        example = {"title": title}
        if abstract:
            example["abstract"] = abstract

        examples.append(example)
        print(f"Added: {title}")

    if not examples:
        print("No reference papers provided.")
        return

    print(f"\nSearching with {len(examples)} reference paper(s)...")

    try:
        results = searcher.search(examples=examples, top_k=20)

        print(f"\nFound {len(results)} similar papers:")
        print("-"*60)
        searcher.display(results, n=10)

        # Save results
        filename = 'reference_search_results.json'
        searcher.save(results, filename)
        print(f"\nResults saved to {filename}")

    except Exception as e:
        print(f"Search failed: {e}")

def search_by_keywords(searcher):
    """Search using keywords"""
    print("\n" + "="*60)
    print("SEARCH BY KEYWORDS")
    print("="*60)
    print("Enter keywords or search query about topics you're interested in\n")

    while True:
        query = input("Enter keywords/search query (or 'quit' to exit): ").strip()
        if query.lower() in ['quit', 'exit', 'q']:
            break

        if not query:
            print("Please enter a search query.")
            continue

        print(f"\nSearching for: '{query}'...")

        try:
            results = searcher.search(query=query, top_k=20)

            if results:
                print(f"\nFound {len(results)} relevant papers:")
                print("-"*60)
                searcher.display(results, n=8)

                # Ask if user wants to save results
                save = input("\nSave these results? (y/n): ").strip().lower()
                if save in ['y', 'yes']:
                    filename = f'keyword_search_{query.replace(" ", "_")[:20]}.json'
                    searcher.save(results, filename)
                    print(f"Results saved to {filename}")
            else:
                print("No relevant papers found.")

        except Exception as e:
            print(f"Search failed: {e}")

        print()  # Add spacing

def show_statistics(searcher):
    """Show dataset statistics"""
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)

    total_papers = len(searcher.papers)
    print(f"Total papers: {total_papers}")

    # Count by decision type if available
    decision_counts = {}
    venue_counts = {}

    for paper in searcher.papers:
        decision = paper.get('decision', 'unknown')
        decision_counts[decision] = decision_counts.get(decision, 0) + 1

        venue = paper.get('venue', 'unknown')
        venue_counts[venue] = venue_counts.get(venue, 0) + 1

    print("\nBy decision type:")
    for decision, count in sorted(decision_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {decision}: {count} papers")

    print("\nBy venue:")
    for venue, count in sorted(venue_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {venue}: {count} papers")

    if len(venue_counts) > 10:
        print(f"  ... and {len(venue_counts) - 10} more venues")

def main():
    """Main demo function"""
    print("This demo supports two search methods:")
    print("1. Search by reference papers")
    print("2. Search by keywords")
    print("3. Show dataset statistics")

    # Initialize searcher (includes file selection)
    searcher = initialize_searcher()
    if not searcher:
        print("Failed to initialize searcher. Exiting.")
        return

    while True:
        print("\n" + "="*40)
        print("MAIN MENU")
        print("="*40)
        print("1. Search by reference papers")
        print("2. Search by keywords")
        print("3. Show dataset statistics")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == '1':
            search_by_reference_papers(searcher)
        elif choice == '2':
            search_by_keywords(searcher)
        elif choice == '3':
            show_statistics(searcher)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

