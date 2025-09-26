"""Validation utilities for input data."""

import re
from pathlib import Path


def validate_query(query: str) -> str:
    """
    Validate and sanitize search query.
    
    Args:
        query: Search query string
        
    Returns:
        Validated query string
        
    Raises:
        ValueError: If query is invalid
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Basic sanitization - remove excessive whitespace
    query = re.sub(r'\s+', ' ', query.strip())
    
    if len(query) > 200:
        raise ValueError("Query too long (maximum 200 characters)")
    
    return query


def validate_filename(filename: str) -> str:
    """
    Validate filename for output files.
    
    Args:
        filename: Filename to validate
        
    Returns:
        Validated filename
        
    Raises:
        ValueError: If filename is invalid
    """
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty")
    
    filename = filename.strip()
    
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        raise ValueError("Filename contains invalid characters")
    
    # Ensure it ends with .csv
    if not filename.lower().endswith('.csv'):
        filename += '.csv'
    
    return filename