import json


def example_service():
    return {"service": "example", "status": "available"}


try:
    from backend.search.search import search_topic
except ImportError:  # pragma: no cover - support running from backend folder
    from search.search import search_topic


if __name__ == "__main__":
    # Test the function to make sure it outputs valid data
    data = search_topic("OpenAI Windsurf")
    print(json.dumps(data, indent=2))