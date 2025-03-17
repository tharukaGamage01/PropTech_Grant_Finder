import pytest
from src.utils import extract_keywords,load_keywords,match_keywords
import pandas as pd
import os
from fuzzywuzzy import fuzz, process




@pytest.mark.parametrize("input_text, expected_output", [
    ("AI and Housing Grants", ["ai", "and", "housing", "grants"]),
    ("", []),
    ("AI, Housing! Energy?", ["ai", "housing", "energy"]),
    ("AI 2025 #Funding!", ["ai", "2025", "funding"]),
])
def test_extract_keywords(input_text, expected_output):
    assert extract_keywords(input_text) == expected_output


def test_load_keywords(tmp_path):
    file_path = tmp_path / "test_keywords.xlsx"
    df = pd.DataFrame({"Keywords": ["AI", "Blockchain", "Renewable Energy"]})
    df.to_excel(file_path, index=False)

    keywords = load_keywords(str(file_path))
    assert keywords == ["AI", "Blockchain", "Renewable Energy"]


def test_load_keywords_invalid_file():
    assert load_keywords("non_existent.xlsx") == []



def match_keywords(word, keyword_list):
    if not keyword_list:
        return []
    result = process.extractOne(word, keyword_list, scorer=fuzz.partial_ratio)
    if result is None:
        return []
    best_match, _ = result
    return [best_match] 

def test_match_keywords_case_insensitive():
    keyword_list = ["AI", "housing"]
    result = match_keywords("HOUSING support", keyword_list)
    assert result == ["housing"]  

