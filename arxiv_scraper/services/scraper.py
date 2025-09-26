"""ArXiv scraper service for fetching and parsing papers."""

import requests
from typing import List
from ..models.paper import Paper


class ArxivScraper:
    """Service class for scraping ArXiv papers."""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self):
        """Initialize the ArXiv scraper."""
        self.session = requests.Session()
    
    def fetch_papers(self, query: str = "generative AI", max_results: int = 5) -> List[Paper]:
        """
        Fetch papers from ArXiv based on query.
        
        Args:
            query: Search query for ArXiv
            max_results: Maximum number of papers to fetch
            
        Returns:
            List of Paper objects
            
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.BASE_URL}?search_query=all:{query}&start=0&max_results={max_results}"
        
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from arXiv: {response.status_code}")
        
        return self._parse_response(response.text)
    
    def _parse_response(self, response_text: str) -> List[Paper]:
        """
        Parse ArXiv API response XML into Paper objects.
        
        Args:
            response_text: Raw XML response from ArXiv API
            
        Returns:
            List of Paper objects
        """
        papers = []
        entries = response_text.split("<entry>")
        
        for entry in entries[1:]:  # Skip first empty entry
            try:
                paper_data = self._extract_paper_data(entry)
                paper = Paper(**paper_data)
                papers.append(paper)
            except (IndexError, ValueError) as e:
                # Skip malformed entries
                print(f"Warning: Skipping malformed entry: {e}")
                continue
        
        return papers
    
    def _extract_paper_data(self, entry: str) -> dict:
        """
        Extract paper data from a single XML entry.
        
        Args:
            entry: Single XML entry string
            
        Returns:
            Dictionary with paper data
        """
        title = entry.split("<title>")[1].split("</title>")[0].strip()
        
        # Extract authors by looking for <name> tags within <author> sections
        authors = []
        author_sections = entry.split("<author>")[1:]
        for section in author_sections:
            if "<name>" in section and "</name>" in section:
                name = section.split("<name>")[1].split("</name>")[0].strip()
                if name:
                    authors.append(name)
        
        abstract = entry.split("<summary>")[1].split("</summary>")[0].strip()
        published = entry.split("<published>")[1].split("</published>")[0].strip()
        
        return {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published": published
        }