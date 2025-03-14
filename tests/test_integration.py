import pytest
from search import search_grants
from ranking import rank_results


# def test_full_search_flow(mocker):
#     mock_results = [
#         {"title": "AI Funding", "snippet": "Apply for AI grants here.", "link": "https://example.com"},
#         {"title": "Tech Grant", "snippet": "Funding available for technology startups.", "link": "https://example.com"}
#     ]
#
#     mocker.patch("search.search_grants", return_value=mock_results)
#
#     keyword_list = ["AI", "Funding", "Technology"]
#     ranked_results = rank_results(mock_results, "AI", keyword_list)
#
#     assert len(ranked_results) == 2
#     assert ranked_results[0]["title"] == "AI Funding"
