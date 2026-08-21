import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def web_search(query):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY is not configured")

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5,
    )

    return [
        {
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content"),
        }
        for result in response.get("results", [])
    ]
