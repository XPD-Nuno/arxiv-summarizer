"""
Main application entry point for the arXiv summarizer.
"""



from summarizer import ArxivSummarizer


def normalize_query(user_input: str) -> str:
    text = (user_input or "").strip()

    if not text:
        return "all:transformer"

    # If user typed a category like "cs.LG" assume cat:<value>
    if "." in text and ":" not in text and " " not in text:
        return f"cat:{text}"

    # If user didn't specify a field (no ":"), assume "all:"
    if ":" not in text:
        return f"all:{text}"

    return text


def main():
    print("=" * 80)
    print("ARXIV SUMMARIZER")
    print("=" * 80)

    raw = input("\nEnter arXiv query or keyword (e.g., transformer, all:transformer, cs.LG): ").strip()
    query = normalize_query(raw)
    print(f"Using query: {query}")

    max_results = input("How many results? (1-10): ").strip()
    try:
        max_results = int(max_results)
        max_results = max(1, min(10, max_results))
    except:
        max_results = 5

    summarizer = ArxivSummarizer()

    # Fetch and parse using the API default max results,
    # so we override Config.MAX_RESULTS by passing max_results into the fetch call.
    # We'll do it by calling the API directly through summarizer.api.
    xml = summarizer.api.fetch(search_query=query, max_results=max_results)
    if not xml:
        print("\nNo data fetched. Try a different query.")
        return

    articles = summarizer.parser.parse(xml)
    if not articles:
        print("\nNo articles found.")
        return

    summarizer.generate_report(articles)
    print("\n✓ Done!")


if __name__ == "__main__":
    main()