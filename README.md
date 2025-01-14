# Arxiv Paper Scraper and Summarizer

This project is a Python script that scrapes the newest papers on generative AI from arxiv and summarizes their abstracts using a pre-trained language model (LLM) like GPT-4. The summarized information is then saved in a structured format, such as a CSV file.

## Setup and Running the Script

1. Clone the repository:
    ```
    git clone https://github.com/githubnext/workspace-blank.git
    cd workspace-blank
    ```

2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Set your OpenAI API key as an environment variable:
    ```
    export OPENAI_API_KEY='your_openai_api_key'
    ```

4. Run the script:
    ```
    python scrape_arxiv.py
    ```

## Dependencies

The script requires the following libraries:
- `requests`
- `json`
- `openai`

You can install them using the provided `requirements.txt` file.
