import pytest
from utils import extract_keywords, load_keywords
import pandas as pd
import os


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
