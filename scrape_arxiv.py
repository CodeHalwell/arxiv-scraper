#!/usr/bin/env python3
"""
Original scrape_arxiv.py - Backward compatibility version.

This file maintains the original function-based interface while using
the new modular structure under the hood.
"""

# Backward compatibility imports - keep original function names
from main import ArxivScraperApp
from arxiv_scraper.config.settings import Settings


def fetch_arxiv_papers(query="generative AI", max_results=5):
    """Original function signature maintained for backward compatibility."""
    app = ArxivScraperApp()
    papers = app.scraper.fetch_papers(query=query, max_results=max_results)
    
    # Convert to original dict format for backward compatibility
    return [{
        "title": paper.title,
        "authors": paper.authors,
        "abstract": paper.abstract,
        "published": paper.published
    } for paper in papers]


def parse_arxiv_response(response):
    """
    Deprecated: This function is kept for backward compatibility only.
    The parsing is now handled internally by ArxivScraper.
    """
    print("Warning: parse_arxiv_response is deprecated. Use ArxivScraper class instead.")
    # For compatibility, we'll return the response as-is
    # In real usage, this would be handled by the new scraper
    return response


def summarize_abstract(abstract):
    """Original function signature maintained for backward compatibility."""
    app = ArxivScraperApp()
    return app.summarizer.generate_summary(abstract)


def save_to_csv(papers, filename="summarized_papers.csv"):
    """Original function signature maintained for backward compatibility."""
    from arxiv_scraper.services.file_manager import FileManager
    from arxiv_scraper.models.paper import Paper
    
    # Convert dict papers back to Paper objects
    paper_objects = []
    for paper_dict in papers:
        # Handle both old and new formats
        authors = paper_dict["authors"]
        if isinstance(authors, str):
            # If authors is already a string (semicolon-separated), split it
            authors = [a.strip() for a in authors.split(";")]
        
        paper_obj = Paper(
            title=paper_dict["title"],
            authors=authors,
            abstract=paper_dict["abstract"],
            published=paper_dict["published"],
            summary=paper_dict.get("summary")
        )
        paper_objects.append(paper_obj)
    
    file_manager = FileManager(output_dir=".")  # Save in current directory like original
    return file_manager.save_to_csv(paper_objects, filename)


def main():
    """Main function - updated to use new modular structure."""
    try:
        app = ArxivScraperApp()
        output_path = app.run()
        print(f"Complete! Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
