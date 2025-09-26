# ArXiv Paper Scraper and Summarizer

This project is a modular Python application that scrapes papers from arXiv and summarizes their abstracts using OpenAI's language models. The application features a clean class-based architecture with Pydantic validation and organized file structure.

## Features

- 🔍 **Modular Architecture**: Clean separation of concerns with dedicated classes for scraping, summarization, and file management
- 📊 **Pydantic Validation**: Type-safe data models with automatic validation
- 🤖 **AI Summarization**: Intelligent abstract summarization using OpenAI's GPT models
- 📁 **Organized Output**: Structured data storage with configurable output directories
- 🔄 **Backward Compatibility**: Original function-based interface still supported
- ⚙️ **Configurable Settings**: Environment-based configuration with sensible defaults

## Project Structure

```
arxiv-scraper/
├── arxiv_scraper/           # Main package
│   ├── __init__.py
│   ├── models/              # Pydantic data models
│   │   ├── __init__.py
│   │   └── paper.py         # Paper model with validation
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   ├── scraper.py       # ArXiv API scraping
│   │   ├── summarizer.py    # AI summarization
│   │   └── file_manager.py  # File I/O operations
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py      # Settings with validation
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── validators.py    # Input validation helpers
├── data/                    # Output directory for results
├── main.py                  # New modular main script
├── scrape_arxiv.py          # Original script (backward compatible)
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CodeHalwell/arxiv-scraper.git
    cd arxiv-scraper
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'
    ```

## Usage

### Using the New Modular Interface (Recommended)

```python
from main import ArxivScraperApp

# Create and run with defaults
app = ArxivScraperApp()
output_path = app.run()

# Or customize the search
output_path = app.run(
    query="machine learning",
    max_results=10,
    filename="ml_papers.csv"
)
```

### Using Individual Components

```python
from arxiv_scraper import ArxivScraper, SummaryGenerator, FileManager

# Initialize services
scraper = ArxivScraper()
summarizer = SummaryGenerator(api_key="your_key")
file_manager = FileManager(output_dir="results")

# Fetch papers
papers = scraper.fetch_papers(query="quantum computing", max_results=5)

# Generate summaries
for paper in papers:
    paper.summary = summarizer.generate_summary(paper.abstract)

# Save results
output_path = file_manager.save_to_csv(papers, "quantum_papers.csv")
```

### Command Line Usage

Run with defaults:
```bash
python main.py
```

Or using the original script (backward compatible):
```bash
python scrape_arxiv.py
```

### Environment Configuration

You can configure the application using environment variables:

```bash
export ARXIV_SCRAPER_DEFAULT_QUERY="deep learning"
export ARXIV_SCRAPER_MAX_RESULTS=10
export ARXIV_SCRAPER_OUTPUT_DIRECTORY="my_papers"
export OPENAI_API_KEY="your_openai_api_key"
```

## Configuration Options

The application supports the following configuration options:

- `ARXIV_SCRAPER_DEFAULT_QUERY`: Default search query (default: "generative AI")
- `ARXIV_SCRAPER_MAX_RESULTS`: Maximum papers to fetch (default: 5, max: 100)
- `ARXIV_SCRAPER_OUTPUT_DIRECTORY`: Output directory for results (default: "data")
- `OPENAI_API_KEY`: Your OpenAI API key for summarization

## Data Models

The application uses Pydantic models for type validation:

```python
class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    published: str
    summary: Optional[str] = None
```

## Error Handling

- **Network Issues**: Gracefully handles ArXiv API connectivity problems
- **API Limits**: Continues without summarization if OpenAI API is unavailable
- **Data Validation**: Automatically validates and sanitizes input data
- **File Operations**: Ensures output directories exist and handles file permissions

## Dependencies

- `requests`: HTTP requests to ArXiv API
- `openai`: OpenAI API integration for summarization
- `pydantic`: Data validation and settings management

## Backward Compatibility

The original `scrape_arxiv.py` script is maintained for backward compatibility but now uses the new modular structure internally. All original function names and signatures are preserved.

## License

This project is open source and available under the MIT License.
