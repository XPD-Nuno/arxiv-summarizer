"""
Unit tests for arXiv summarizer project.
Run with: pytest -v
"""

import requests
from unittest.mock import Mock, patch
import pytest

from arxiv_api import ArxivAPI
from parser import ArxivParser


SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/1234.5678v1</id>
    <title>Test Paper Title</title>
    <summary>This is a test abstract.</summary>
    <published>2026-01-01T00:00:00Z</published>
    <updated>2026-01-02T00:00:00Z</updated>
    <author><name>Jane Doe</name></author>
    <author><name>John Smith</name></author>
    <category term="cs.AI"/>
    <category term="cs.LG"/>
    <link href="http://arxiv.org/abs/1234.5678v1" rel="alternate" type="text/html"/>
  </entry>
</feed>
"""


class TestArxivAPI:
    def test_build_query_url_basic(self):
        api = ArxivAPI()
        url = api.build_query_url(search_query="all:transformer", start=0, max_results=3)
        assert "search_query=all%3Atransformer" in url
        assert "start=0" in url
        assert "max_results=3" in url

    def test_build_query_url_with_sort(self):
        api = ArxivAPI()
        url = api.build_query_url(
            search_query="cat:cs.LG",
            start=5,
            max_results=2,
            sort_by="submittedDate",
            sort_order="descending",
        )
        assert "search_query=cat%3Acs.LG" in url
        assert "start=5" in url
        assert "max_results=2" in url
        assert "sortBy=submittedDate" in url
        assert "sortOrder=descending" in url

    @patch("arxiv_api.requests.get")
    def test_fetch_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_XML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = ArxivAPI()
        xml = api.fetch(search_query="all:test", start=0, max_results=1)
        assert xml.startswith("<?xml")
        assert "<feed" in xml

    @patch("arxiv_api.requests.get")
    def test_fetch_failure_returns_empty_string(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        api = ArxivAPI()
        xml = api.fetch(search_query="all:test", start=0, max_results=1)
        assert xml == ""


class TestArxivParser:
    def test_parse_returns_articles(self):
        parser = ArxivParser()
        articles = parser.parse(SAMPLE_XML)
        assert len(articles) == 1

        article = articles[0]
        assert article["id"] == "http://arxiv.org/abs/1234.5678v1"
        assert article["title"] == "Test Paper Title"
        assert "test abstract" in article["summary"].lower()
        assert article["published"] == "2026-01-01T00:00:00Z"
        assert article["updated"] == "2026-01-02T00:00:00Z"
        assert article["authors"] == ["Jane Doe", "John Smith"]
        assert "cs.AI" in article["categories"]
        assert "cs.LG" in article["categories"]
        assert article["link"]  # should not be empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])