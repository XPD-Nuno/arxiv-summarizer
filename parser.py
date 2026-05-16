"""
Parser module for arXiv Atom XML responses.
"""

import feedparser


class ArxivParser:
    """Parse arXiv Atom feed into structured data."""

    def parse(self, xml_data: str):
        """
        Parse XML string into a list of article dictionaries.

        Args:
            xml_data: Raw XML from arXiv API

        Returns:
            List of dictionaries (articles)
        """
        feed = feedparser.parse(xml_data)

        articles = []

        for entry in feed.entries:
            article = {
                "id": entry.get("id", ""),
                "title": entry.get("title", "").strip(),
                "summary": entry.get("summary", "").strip(),
                "authors": [author.name for author in entry.get("authors", [])],
                "published": entry.get("published", ""),
                "updated": entry.get("updated", ""),
                "categories": [tag["term"] for tag in entry.get("tags", [])],
                "link": entry.get("link", ""),
            }
            articles.append(article)

        print(f"✓ Parsed {len(articles)} articles")
        return articles


if __name__ == "__main__":
    from arxiv_api import ArxivAPI

    api = ArxivAPI()
    parser = ArxivParser()

    xml = api.fetch(search_query="all:transformer", max_results=3)

    if xml:
        articles = parser.parse(xml)

        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"Authors: {', '.join(article['authors'])}")
            print(f"Published: {article['published']}")