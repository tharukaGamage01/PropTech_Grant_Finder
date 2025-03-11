import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def search_grants(query):
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        raise ValueError("Missing API keys. Ensure GOOGLE_API_KEY and SEARCH_ENGINE_ID are set in .env")

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", "")
            })
    return results
