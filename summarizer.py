"""
Simple arXiv summarizer module.

Processes parsed articles and creates a readable report.
"""

from arxiv_api import ArxivAPI
from parser import ArxivParser


class ArxivSummarizer:
    """Main summarizer class."""

    def __init__(self):
        self.api = ArxivAPI()
        self.parser = ArxivParser()

    def fetch_and_parse(self, query: str):
        """Fetch and parse articles from arXiv."""
        xml = self.api.fetch(search_query=query)

        if not xml:
            print("No data fetched.")
            return []

        articles = self.parser.parse(xml)
        return articles

    def generate_report(self, articles):
        """Generate a simple report."""
        print("\n" + "=" * 80)
        print("ARXIV SEARCH REPORT")
        print("=" * 80)

        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"Authors: {', '.join(article['authors'])}")
            print(f"Published: {article['published']}")
            print(f"Link: {article['link']}")

            # Short summary (first 200 chars)
            short_summary = article["summary"][:200].replace("\n", " ")
            print(f"\nSummary: {short_summary}...")

            print("\n" + "-" * 80)


if __name__ == "__main__":
    summarizer = ArxivSummarizer()

    # Example query
    query = "all:transformer"

    articles = summarizer.fetch_and_parse(query)

    if articles:
        summarizer.generate_report(articles)
    else:
        print("No articles found.")