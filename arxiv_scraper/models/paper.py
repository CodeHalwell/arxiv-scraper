"""Pydantic model for ArXiv paper data."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class Paper(BaseModel):
    """Model representing an ArXiv paper with metadata and summary."""
    
    title: str = Field(..., min_length=1, description="The paper's title")
    authors: List[str] = Field(..., min_items=1, description="List of paper authors")
    abstract: str = Field(..., min_length=1, description="The paper's abstract")
    published: str = Field(..., description="Publication date as string")
    summary: Optional[str] = Field(None, description="AI-generated summary of the abstract")
    
    @validator('title', 'abstract')
    def strip_whitespace(cls, v):
        """Strip leading and trailing whitespace from title and abstract."""
        return v.strip() if v else v
    
    @validator('authors')
    def validate_authors(cls, v):
        """Ensure authors list contains valid names."""
        if not v:
            raise ValueError("Authors list cannot be empty")
        # Strip whitespace from each author name
        return [author.strip() for author in v if author.strip()]
    
    def to_dict(self) -> dict:
        """Convert paper to dictionary for CSV export."""
        return {
            "title": self.title,
            "authors": "; ".join(self.authors),  # Join authors with semicolon for CSV
            "abstract": self.abstract,
            "published": self.published,
            "summary": self.summary or ""
        }
    
    class Config:
        """Pydantic configuration."""
        str_strip_whitespace = True
        validate_assignment = True