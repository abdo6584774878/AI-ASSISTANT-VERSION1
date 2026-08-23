import os
import re

from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def _clean_url(url):
    if not url:
        return ""

    markdown_match = re.match(
        r"\[([^\]]+)\]\(([^)]+)\)",
        url,
    )

    if markdown_match:
        return markdown_match.group(2)

    return url


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

    cleaned_results = []

    for result in response.get("results", []):
        url = _clean_url(result.get("url", ""))

        content = result.get("content", "")

        if content:
            content = content[:2000]

        cleaned_results.append(
            {
                "title": result.get("title"),
                "url": url,
                "source": urlparse(url).netloc,
                "content": content,
            }
        )

    return cleaned_results
