import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from src.utils import extract_keywords

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def rank_results(results, keywords, keyword_list):
    if not results:
        return []

    if not isinstance(keywords, list):
        raise ValueError("Keywords should be a list.")
    
    keyword_list = keyword_list or []  
    
    extracted_keywords = []
    for keyword in keywords:
        if isinstance(keyword, str) and keyword.strip():
            extracted_keywords.extend(extract_keywords(keyword.strip()))

    if not extracted_keywords:
        return results

    combined_keywords = " ".join(set(extracted_keywords + keyword_list)).strip()
    if not combined_keywords:
        return results

    texts = [r.get("title", "").strip() + " " + r.get("snippet", "").strip() for r in results]
    texts = [t for t in texts if t.strip()]  

    if not texts:
        return results

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts + [combined_keywords])
        cosine_similarities = (tfidf_matrix * tfidf_matrix.T).A[-1][:-1]
        ranked_results = sorted(zip(results, cosine_similarities), key=lambda x: x[1], reverse=True)
        return [r[0] for r in ranked_results]
    except ValueError as e:
        print(f"Error in TF-IDF processing: {e}")
        return results
