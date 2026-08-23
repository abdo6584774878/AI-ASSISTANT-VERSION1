from assistant.tools.web import web_search


def test_web_search_requires_api_key(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)

    try:
        web_search("Python")
    except ValueError as error:
        assert str(error) == "TAVILY_API_KEY is not configured"
    else:
        raise AssertionError("web_search should require an API key")


def test_web_search_rejects_empty_query(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    try:
        web_search("")
    except ValueError as error:
        assert str(error) == "Search query cannot be empty"
    else:
        raise AssertionError("web_search should reject an empty query")


def test_web_search_returns_clean_results(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def search(self, query, search_depth, max_results):
            assert query == "Python"
            assert search_depth == "basic"
            assert max_results == 5

            return {
                "results": [
                    {
                        "title": "Python",
                        "url": "https://python.org",
                        "source": "python.org",
                        "content": "Python is a programming language.",
                    }
                ]
            }

    monkeypatch.setattr(
        "assistant.tools.web.TavilyClient",
        FakeClient,
    )

    result = web_search("Python")

    assert result == [
        {
            "title": "Python",
            "url": "https://python.org",
            "source": "python.org",
            "content": "Python is a programming language.",
        }
    ]


def test_web_search_truncates_content(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def search(self, query, search_depth, max_results):
            return {
                "results": [
                    {
                        "title": "Python",
                        "url": "https://python.org",
                        "content": "A" * 5000,
                    }
                ]
            }

    monkeypatch.setattr(
        "assistant.tools.web.TavilyClient",
        FakeClient,
    )

    result = web_search("Python")

    assert len(result) == 1
    assert len(result[0]["content"]) == 2000


def test_web_search_returns_source(monkeypatch):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def search(self, query, search_depth, max_results):
            return {
                "results": [
                    {
                        "title": "Python",
                        "url": "https://python.org/about/",
                        "content": "Python is a programming language.",
                    }
                ]
            }

    monkeypatch.setattr(
        "assistant.tools.web.TavilyClient",
        FakeClient,
    )

    result = web_search("Python")

    assert result == [
        {
            "title": "Python",
            "url": "https://python.org/about/",
            "source": "python.org",
            "content": "Python is a programming language.",
        }
    ]
