import os
import requests
import logging
import streamlit as st
from urllib.parse import quote_plus 

logging.basicConfig(level=logging.ERROR)

PRETRAINED_GRANT_SOURCES = [
    {
        "title": "Tech Startup Grant - USA",
        "link": "https://example.com/tech-grant",
        "snippet": "A funding opportunity for AI and technology startups in the USA."
    },
    {
        "title": "EU Innovation Grant",
        "link": "https://europa.eu/grants",
        "snippet": "Funding support for European technology projects."
    },
    {
        "title": "Green Energy Grant - UK",
        "link": "https://gov.uk/green-energy-grant",
        "snippet": "Government grant for renewable energy startups in the UK."
    }
]

def fallback_grant_sources():
    return PRETRAINED_GRANT_SOURCES

def search_google_grants(query):
   
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", None)
    SEARCH_ENGINE_ID = st.secrets.get("SEARCH_ENGINE_ID", None)
    
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        logging.error("Missing API keys for Google Search.")
        return []
    
    encoded_query = quote_plus(query)
    url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": item.get("title", "No title"),
                "link": item.get("link", "#"),
                "snippet": item.get("snippet", "No description available.")
            }
            for item in data.get("items", [])
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Google API request failed: {e}")
        return []

def search_grants_gov():
    url = "https://www.grants.gov/grantsws/rest/opportunities/search"
    params = {"keyword": "grant", "oppStatus": "open", "startRecordNum": 1, "rows": 10}
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": item.get("title", "No title"),
                "link": item.get("synopsisURL", "#"),
                "snippet": item.get("agencyName", "No description available.")
            }
            for item in data.get("opportunityDetails", [])
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"Grants.gov API request failed: {e}")
        return []

def search_uk_gov_grants():
    url = "https://www.gov.uk/api/content/business-finance-support"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": item.get("title", "No title"),
                "link": f"https://www.gov.uk{item.get('web_url', '#')}",
                "snippet": item.get("description", "No description available.")
            }
            for item in data.get("details", {}).get("business_finance_support", [])
        ]
    except requests.exceptions.RequestException as e:
        logging.error(f"UK Gov API request failed: {e}")
        return []

def search_grants(query):
    results = search_google_grants(query)
    if not results:
        logging.info("No results from Google, trying Grants.gov")
        results = search_grants_gov()
    if not results:
        logging.info("No results from Grants.gov, trying UK Gov grants")
        results = search_uk_gov_grants()
    if not results:
        logging.info("No results from UK Gov, using fallback sources")
        results = fallback_grant_sources()
    return results
