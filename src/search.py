import os
import requests
import logging
from dotenv import load_dotenv
from urllib.parse import quote_plus  
load_dotenv()


logging.basicConfig(level=logging.ERROR)

def search_grants(query):
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SEARCH_ENGINE_ID = st.secrets["SEARCH_ENGINE_ID"]

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        raise ValueError("Missing API keys. Ensure GOOGLE_API_KEY and SEARCH_ENGINE_ID are set in .env")

    
    encoded_query = quote_plus(query)
    url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return []  

    results = [
        {
            "title": item.get("title", "No title"),
            "link": item.get("link", "#"),
            "snippet": item.get("snippet", "No description available.")
        }
        for item in data.get("items", [])
    ]
    
    return results
