import requests
import json
import openai
import csv

def fetch_arxiv_papers(query="generative AI", max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from arxiv")
    return response.text

def parse_arxiv_response(response):
    papers = []
    entries = response.split("<entry>")
    for entry in entries[1:]:
        title = entry.split("<title>")[1].split("</title>")[0].strip()
        authors = [author.split("</name>")[0].strip() for author in entry.split("<author>")[1:]]
        abstract = entry.split("<summary>")[1].split("</summary>")[0].strip()
        published = entry.split("<published>")[1].split("</published>")[0].strip()
        papers.append({
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published": published
        })
    return papers

def summarize_abstract(abstract):
    openai.api_key = "YOUR_OPENAI_API_KEY"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following abstract:\n\n{abstract}",
        max_tokens=150
    )
    summary = response.choices[0].text.strip()
    return summary

def save_to_csv(papers, filename="summarized_papers.csv"):
    keys = papers[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(papers)

def main():
    response = fetch_arxiv_papers()
    papers = parse_arxiv_response(response)
    for paper in papers:
        paper["summary"] = summarize_abstract(paper["abstract"])
    save_to_csv(papers)

if __name__ == "__main__":
    main()
