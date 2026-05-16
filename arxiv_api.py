"""
arXiv API integration module.

This module fetches raw Atom XML from the arXiv API endpoint.
"""

import time
import requests
from config import Config


class ArxivAPI:
    """Fetch papers from arXiv via the export API."""

    def __init__(self):
        self.base_url = Config.ARXIV_BASE_URL
        self.last_call_time = 0.0

    def _wait_if_needed(self):
        """Wait to respect a minimum delay between requests."""
        elapsed = time.time() - self.last_call_time
        if elapsed < Config.REQUEST_DELAY:
            wait_time = Config.REQUEST_DELAY - elapsed
            print(f"Rate limiting arXiv: waiting {wait_time:.2f}s...")
            time.sleep(wait_time)
        self.last_call_time = time.time()

    def build_query_url(
        self,
        search_query: str,
        start: int = 0,
        max_results: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> str:
        """
        Build a query URL for arXiv.

        Args:
            search_query: arXiv search query string, e.g. 'all:transformer'
            start: 0-based result offset
            max_results: number of results to return
            sort_by: e.g. 'relevance', 'lastUpdatedDate', 'submittedDate'
            sort_order: 'ascending' or 'descending'

        Returns:
            Full query URL (string).
        """
        if max_results is None:
            max_results = Config.MAX_RESULTS

        params = {
            "search_query": search_query,
            "start": start,
            "max_results": max_results,
        }

        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order

        # requests will build the final URL when sending, but for debugging it's useful
        query_string = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
        return f"{self.base_url}?{query_string}"

    def fetch(self, search_query: str, start: int = 0, max_results: int | None = None) -> str:
        """
        Fetch raw Atom XML from arXiv.

        Args:
            search_query: Query string such as 'all:electron' or 'cat:cs.LG'
            start: Result offset
            max_results: Page size

        Returns:
            Raw XML feed as a string. Returns empty string on failure.
        """
        self._wait_if_needed()

        url = self.build_query_url(search_query=search_query, start=start, max_results=max_results)
        try:
            response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            print("✓ Fetched arXiv feed successfully")
            return response.text
        except requests.exceptions.RequestException as exc:
            print(f"✗ Error fetching arXiv feed: {exc}")
            return ""


if __name__ == "__main__":
    api = ArxivAPI()

    # Example: fetch a few results about "transformer" in all fields
    xml = api.fetch(search_query="all:transformer", start=0, max_results=3)

    if xml:
        print("\n--- XML Preview (first 500 chars) ---")
        print(xml[:500])