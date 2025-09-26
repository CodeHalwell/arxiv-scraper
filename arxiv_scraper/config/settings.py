"""Configuration settings using Pydantic."""

import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # ArXiv API settings
    default_query: str = Field(default="generative AI", description="Default search query")
    max_results: int = Field(default=5, ge=1, le=100, description="Maximum papers to fetch")
    
    # OpenAI settings
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    summary_max_tokens: int = Field(default=150, ge=50, le=500, description="Maximum tokens for summaries")
    
    # File settings
    output_directory: str = Field(default="data", description="Output directory for files")
    default_filename: str = Field(default="summarized_papers.csv", description="Default output filename")
    
    @field_validator('openai_api_key', mode='before')
    @classmethod
    def validate_openai_api_key(cls, v):
        """Ensure backward compatibility with OPENAI_API_KEY environment variable."""
        if not v:
            # If no prefixed env var is set, check for the standard OPENAI_API_KEY
            return os.getenv("OPENAI_API_KEY", "")
        return v
    
    model_config = {
        "env_prefix": "ARXIV_SCRAPER_",
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }