import pytest
from src.ranking import rank_results

def test_empty():
    assert rank_results([], ["AI"], ["AI", "Tech"]) == []

def test_single():
    results = [{"title": "AI Grant", "snippet": "Funding for AI research."}]
    ranked = rank_results(results, ["AI"], ["AI", "Funding"])
    assert ranked == results  

def test_multiple():
    results = [
        {"title": "AI Research Funding", "snippet": "Supports AI innovation."},
        {"title": "Renewable Energy Grant", "snippet": "Funds clean energy projects."},
        {"title": "Tech and AI Grants", "snippet": "Funding for technology and AI."},
        {"title": "General Science Grant", "snippet": "Available for all scientific fields."}
    ]
    
    ranked = rank_results(results, ["AI"], ["AI", "Tech", "Funding"])
    
    expected = [
        {"title": "AI Research Funding", "snippet": "Supports AI innovation."},
        {"title": "Tech and AI Grants", "snippet": "Funding for technology and AI."},
        {"title": "Renewable Energy Grant", "snippet": "Funds clean energy projects."},
        {"title": "General Science Grant", "snippet": "Available for all scientific fields."}
    ]
    
    assert ranked == expected  

def test_no_keywords():
    results = [{"title": "AI Grant", "snippet": "Funding"}]
    ranked = rank_results(results, [], ["AI", "Funding"])
    assert ranked == results  

def test_invalid_keywords():
    with pytest.raises(ValueError, match="Keywords should be a list."):
        rank_results([{"title": "AI Grant", "snippet": "Funding"}], "AI", ["AI", "Funding"])

def test_no_match():
    results = [
        {"title": "Wildlife Grant", "snippet": "Funding for animals."},
        {"title": "History Grant", "snippet": "Preserving historic sites."}
    ]
    
    ranked = rank_results(results, ["AI"], ["AI", "Tech"])
    
    assert ranked == results  

def test_tfidf_fail():
    results = [{"title": "", "snippet": ""}]  
    ranked = rank_results(results, ["AI"], ["AI", "Funding"])
    assert ranked == results  # Should return unranked results instead of failing
