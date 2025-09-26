"""AI summarization service for paper abstracts."""

import os
from typing import Optional
import openai
from openai import OpenAI


class SummaryGenerator:
    """Service class for generating AI summaries of paper abstracts."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the summary generator with OpenAI API.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY":
            print("Warning: No valid OpenAI API key found. Summaries will be skipped.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate_summary(self, abstract: str) -> Optional[str]:
        """
        Generate a summary for the given abstract.
        
        Args:
            abstract: The paper abstract to summarize
            
        Returns:
            Generated summary or None if API is not available
        """
        if not self.client or not abstract.strip():
            return None
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Updated to use newer chat model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes academic paper abstracts concisely."
                    },
                    {
                        "role": "user", 
                        "content": f"Summarize the following abstract in 2-3 sentences:\n\n{abstract}"
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Warning: Failed to generate summary: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if the summarization service is available."""
        return self.client is not None