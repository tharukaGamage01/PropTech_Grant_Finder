import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def search_grants(query):
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        raise ValueError("Missing API keys. Ensure GOOGLE_API_KEY and SEARCH_ENGINE_ID are set in .env")

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title", "No title"),
            "link": item.get("link", "#"),
            "snippet": item.get("snippet", "No description available.")
        })
    return results
