from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """Runs a DuckDuckGo search and returns results formatted as plain text."""
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No search results found."
        formatted = []
        for r in results:
            formatted.append(f"- {r['title']}: {r['body']} (Source: {r['href']})")
        return "\n".join(formatted)
    except Exception as e:
        return f"Search failed: {e}"

if __name__ == "__main__":
    print(web_search("flights from Kannur to Tokyo October price"))