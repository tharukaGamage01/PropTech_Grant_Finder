import pytest
from ranking import rank_results


def test_rank_results_empty():
    assert rank_results([], "AI", ["AI", "Technology"]) == []


# def test_rank_results_single():
#     results = [{"title": "AI Grant", "snippet": "Funding for AI research."}]
#     ranked = rank_results(results, "AI", ["AI", "Funding"])
#     assert ranked == results


def test_rank_results_no_keyword():

    with pytest.raises(ValueError, match="Keyword cannot be empty."):
        rank_results([{"title": "AI Grant", "snippet": "Funding"}], "", ["AI", "Funding"])
