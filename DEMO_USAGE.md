# Demo Usage Guide

## Overview

The enhanced demo now supports two search methods plus dataset statistics, making it easier to find relevant papers in your collection.

## Quick Start

```bash
python demo.py
```

**New Feature**: Interactive file selection from `crawled_papers` directory!

## Features

### 1. Search by Reference Papers

Find papers similar to ones you already like.

**How it works:**
- Enter titles and abstracts of reference papers
- System uses semantic similarity to find related papers
- Great for finding related work and similar research

**Example session:**
```
Enter paper title: Deep Learning for Computer Vision
Enter paper abstract: This paper presents a novel approach to image classification using deep neural networks...
Added: Deep Learning for Computer Vision

Enter paper title: [Press Enter to finish]

Searching with 1 reference paper(s)...

Found 20 similar papers:
------------------------------------------------------------
1. [0.8945] Neural Networks for Image Recognition
   #12345 | computer_vision
   https://openreview.net/forum?id=abc123

2. [0.8732] Advanced Computer Vision Techniques
   #12346 | computer_vision
   https://openreview.net/forum?id=def456
...
```

**Use cases:**
- Find papers similar to your own work
- Discover related research in your field
- Find follow-up work on specific topics

### 2. Search by Keywords

Find papers on specific topics using keywords or natural language queries.

**How it works:**
- Enter keywords or search queries
- System finds papers matching those topics
- Great for exploring research areas

**Example session:**
```
Enter keywords/search query: transformer architecture attention mechanism

Searching for: 'transformer architecture attention mechanism'...

Found 20 relevant papers:
------------------------------------------------------------
1. [0.9123] Attention Is All You Need
   #23456 | natural_language_processing
   https://openreview.net/forum?id=ghi789

2. [0.8891] BERT: Pre-training of Deep Bidirectional Transformers
   #23457 | natural_language_processing
   https://openreview.net/forum?id=jkl012
...

Save these results? (y/n): y
Results saved to keyword_search_transformer_architecture_atte.json
```

**Use cases:**
- Explore specific research topics
- Find papers on particular techniques
- Discover papers in specific domains

### 3. Dataset Statistics

Get an overview of your paper collection.

**Example output:**
```
DATASET STATISTICS
============================================================
Total papers: 1,387

By decision type:
  poster: 1,000 papers
  spotlight: 326 papers
  oral: 61 papers

By venue:
  NeurIPS 2024 poster: 1,000 papers
  NeurIPS 2024 spotlight: 326 papers
  NeurIPS 2024 oral: 61 papers
```

## Tips for Effective Search

### Reference Papers Search
- **Be specific**: Use complete, accurate titles
- **Add abstracts**: Including abstracts improves accuracy
- **Multiple references**: Add 2-3 reference papers for better results
- **Mix topics**: Combine papers from different but related areas

### Keywords Search
- **Use technical terms**: "attention mechanism" vs "how models work"
- **Combine concepts**: "graph neural networks drug discovery"
- **Try variations**: "deep learning" vs "neural networks" vs "machine learning"
- **Be specific**: "computer vision medical imaging" vs "computer vision"

## File Management

**Automatic saving:**
- Reference paper results: `reference_search_results.json`
- Keyword search results: `keyword_search_[query].json`

**File format:**
```json
{
  "model": "bge-m3",
  "total": 20,
  "results": [
    {
      "paper": {
        "id": "paper_id",
        "title": "Paper Title",
        "authors": ["Author 1", "Author 2"],
        "abstract": "Paper abstract...",
        "keywords": ["keyword1", "keyword2"],
        "venue": "Conference Year decision",
        "decision": "poster",
        "forum_url": "https://openreview.net/forum?id=paper_id"
      },
      "similarity": 0.8945
    }
  ]
}
```

## Programming Interface

You can also use the demo functions programmatically:

```python
from demo import initialize_searcher, search_by_keywords, search_by_reference_papers

# Initialize searcher
searcher = initialize_searcher()

# Search by keywords
search_by_keywords(searcher)

# Search by reference papers
search_by_reference_papers(searcher)
```

## Troubleshooting

**Common issues:**

1. **"No papers JSON file found"**
   - Run the crawler first: `python multi_conference_crawler.py`
   - Check that papers files exist in current directory

2. **"Search failed"**
   - Check internet connection
   - Verify API key is correctly configured
   - Try re-running the demo

3. **Poor search results**
   - Try more specific keywords
   - Use complete paper titles
   - Add abstracts to reference papers
   - Use multiple reference papers

**Getting help:**
- Check the SETUP.md file for configuration details
- Verify your .env file contains the correct API key
- Ensure all dependencies are installed: `pip install -r requirements.txt`