#!/usr/bin/env python3
"""
Main script for the ArXiv Scraper - Modular implementation.

This script provides the same functionality as the original scrape_arxiv.py
but uses a modular class-based structure with Pydantic validation.
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from arxiv_scraper.services.scraper import ArxivScraper
from arxiv_scraper.services.summarizer import SummaryGenerator
from arxiv_scraper.services.file_manager import FileManager
from arxiv_scraper.config.settings import Settings
from arxiv_scraper.utils.validators import validate_query, validate_filename


class ArxivScraperApp:
    """Main application class for ArXiv scraping and summarization."""
    
    def __init__(self, settings: Settings = None):
        """
        Initialize the application with services.
        
        Args:
            settings: Configuration settings. If None, uses defaults.
        """
        self.settings = settings or Settings()
        self.scraper = ArxivScraper()
        self.summarizer = SummaryGenerator(api_key=self.settings.openai_api_key)
        self.file_manager = FileManager(output_dir=self.settings.output_directory)
    
    def run(self, query: str = None, max_results: int = None, filename: str = None) -> str:
        """
        Run the complete scraping and summarization process.
        
        Args:
            query: Search query (uses default if None)
            max_results: Maximum results (uses default if None)
            filename: Output filename (uses default if None)
            
        Returns:
            Path to the saved CSV file
        """
        # Use defaults from settings if not provided
        query = query or self.settings.default_query
        max_results = max_results or self.settings.max_results
        filename = filename or self.settings.default_filename
        
        # Validate inputs
        query = validate_query(query)
        filename = validate_filename(filename)
        
        print(f"Fetching papers for query: '{query}' (max {max_results} results)")
        
        # Fetch papers
        papers = self.scraper.fetch_papers(query=query, max_results=max_results)
        print(f"Found {len(papers)} papers")
        
        # Generate summaries if API is available
        if self.summarizer.is_available():
            print("Generating AI summaries...")
            for i, paper in enumerate(papers, 1):
                print(f"Summarizing paper {i}/{len(papers)}: {paper.title[:50]}...")
                paper.summary = self.summarizer.generate_summary(paper.abstract)
        else:
            print("OpenAI API not available - skipping summarization")
            for paper in papers:
                paper.summary = None
        
        # Save to CSV
        output_path = self.file_manager.save_to_csv(papers, filename)
        
        return output_path


def main():
    """Main entry point - maintains backward compatibility with original script."""
    try:
        app = ArxivScraperApp()
        output_path = app.run()
        print(f"Complete! Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()