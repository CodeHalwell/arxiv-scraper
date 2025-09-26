"""File management service for saving papers to various formats."""

import csv
import os
from pathlib import Path
from typing import List
from ..models.paper import Paper


class FileManager:
    """Service class for managing file operations."""
    
    def __init__(self, output_dir: str = "data"):
        """
        Initialize file manager with output directory.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_to_csv(self, papers: List[Paper], filename: str = "summarized_papers.csv") -> str:
        """
        Save papers to CSV file.
        
        Args:
            papers: List of Paper objects to save
            filename: Output filename
            
        Returns:
            Full path to the saved file
            
        Raises:
            ValueError: If papers list is empty
        """
        if not papers:
            raise ValueError("Cannot save empty papers list to CSV")
        
        filepath = self.output_dir / filename
        
        # Convert papers to dictionaries for CSV writing
        paper_dicts = [paper.to_dict() for paper in papers]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
            fieldnames = paper_dicts[0].keys()
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(paper_dicts)
        
        print(f"Saved {len(papers)} papers to {filepath}")
        return str(filepath)
    
    def get_output_path(self, filename: str) -> str:
        """
        Get full path for output file.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full path to the file
        """
        return str(self.output_dir / filename)