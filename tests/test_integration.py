import pytest
from unittest.mock import patch
from src.search import search_grants
from src.ranking import rank_results

def test_full_search_flow():
    mock_results = [
        {"title": "AI Funding", "snippet": "Apply for AI grants here.", "link": "https://example.com"},
        {"title": "Tech Grant", "snippet": "Funding available for technology startups.", "link": "https://example.com"}
    ]

    with patch("src.search.search_grants", return_value=mock_results):
        keyword_list = ["AI", "Funding", "Technology"]
        ranked_results = rank_results(mock_results, ["AI"], keyword_list)

        assert len(ranked_results) == 2
        assert ranked_results[0]["title"] == "AI Funding" 
@patch("src.search.search_grants")
def test_partial_keyword_match(mock_search):
    mock_results = [
        {"title": "AI Funding", "snippet": "Funding for AI research.", "link": "https://example.com"},
        {"title": "General Tech Grant", "snippet": "Funding for technology-related projects.", "link": "https://example.com"},
        {"title": "Startup Support", "snippet": "Grants available for new businesses.", "link": "https://example.com"}
    ]

    mock_search.return_value = mock_results

    keyword_list = ["AI", "Funding", "Technology"]
    ranked_results = rank_results(mock_results, ["AI"], keyword_list)

    assert len(ranked_results) == 3
    assert ranked_results[0]["title"] == "AI Funding"  # Exact match should rank highest
    assert ranked_results[1]["title"] == "General Tech Grant"  # Partial match should be second
    assert ranked_results[2]["title"] == "Startup Support"  # Least relevant should be last
