# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

The crawler now uses the BGE-M3 embedding API for high-quality paper search. Your API key has been pre-configured in the `.env` file.

**.env file contents:**
```
EMBEDDING_API_KEY=sk-dadjnrsjq3igueus
```

### 3. Run the Paper Crawler

```bash
python multi_conference_crawler.py
```

Follow the prompts to:
1. Select a conference (NeurIPS, ICML, ICLR, AAAI, CVPR, ICCV, ECCV, ACL, EMNLP, NAACL)
2. Enter a year (any year between 2000-2030)
3. Choose an output directory

### 4. Search Papers

After crawling, use the search functionality:

```bash
python demo.py
```

This will automatically:
- Find your crawled papers file
- Use the configured API for embeddings
- Provide search examples

## Configuration

### API Configuration

The system supports three embedding methods:

1. **API (Recommended)**: BGE-M3 model via Infini-AI
   - Uses your pre-configured API key
   - High quality 1024-dimensional embeddings
   - Fast and reliable

2. **Local**: SentenceTransformer model
   - Free, no API required
   - Lower quality but functional
   - Slower for large datasets

3. **OpenAI**: GPT embeddings
   - Requires separate OpenAI API key
   - High quality but costs money

### Custom Configuration

You can modify the `.env` file:

```env
# Primary embedding API (pre-configured)
EMBEDDING_API_KEY=sk-dadjnrsjq3igueus

# Optional: Custom API URL
EMBEDDING_API_URL=https://cloud.infini-ai.com/maas/v1/embeddings

# Optional: OpenAI API key (if using OpenAI embeddings)
OPENAI_API_KEY=your_openai_key_here
```

## Usage Examples

### Programmatic Usage

```python
from search import PaperSearcher

# Using the configured API (recommended)
searcher = PaperSearcher('papers.json', model_type='api')

# Compute embeddings
searcher.compute_embeddings()

# Search by query
results = searcher.search(query="machine learning", top_k=10)

# Search by example papers
examples = [{
    "title": "Deep Learning for NLP",
    "abstract": "A novel approach to natural language processing..."
}]
results = searcher.search(examples=examples, top_k=10)

# Display results
searcher.display(results, n=5)
```

### Batch Crawling

```python
from multi_conference_crawler import MultiConferenceCrawler

crawler = MultiConferenceCrawler()

# Crawl multiple conferences
conferences = [
    ("NeurIPS", 2024),
    ("ICML", 2024),
    ("ICLR", 2024)
]

for conf, year in conferences:
    papers_by_decision, all_papers = crawler.crawl_conference_by_decision(
        conference=conf, year=year, output_dir="papers"
    )
```

## File Structure

After crawling, you'll get:

```
output_dir/
├── conference_year/
│   ├── conference_year_oral.json      # Oral presentations
│   ├── conference_year_spotlight.json # Spotlight presentations
│   ├── conference_year_poster.json    # Poster presentations
│   └── conference_year_all.json       # All papers combined
```

Each paper contains:
- `id`: Unique identifier
- `title`: Paper title
- `authors`: List of authors
- `abstract`: Paper abstract
- `keywords`: Paper keywords
- `primary_area`: Research area
- `venue`: Conference venue
- `decision`: Acceptance decision
- `forum_url`: Paper discussion URL

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists in the project directory
   - Check that `EMBEDDING_API_KEY` is correctly set

2. **Network Issues**
   - Check internet connection
   - Verify API endpoint is accessible

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure Python 3.7+ is installed

### Support

For issues with:
- **API Key**: Contact your API provider
- **Crawler Logic**: Check the logs for detailed error messages
- **Search Functionality**: Verify paper files exist and are properly formatted