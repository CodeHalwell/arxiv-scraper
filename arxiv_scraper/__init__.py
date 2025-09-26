"""ArXiv Scraper Package - Modular structure for scraping and summarizing ArXiv papers."""

from .models.paper import Paper
from .services.scraper import ArxivScraper
from .services.summarizer import SummaryGenerator
from .services.file_manager import FileManager

__version__ = "1.0.0"
__all__ = ["Paper", "ArxivScraper", "SummaryGenerator", "FileManager"]