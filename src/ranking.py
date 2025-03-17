import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import extract_keywords

def rank_results(results, keywords, keyword_list):
    if not results:
        return []

    if not isinstance(keywords, list):
        raise ValueError("Keywords should be a list.")

    extracted_keywords = []
    for keyword in keywords:
        if isinstance(keyword, str) and keyword.strip():
            extracted_keywords.extend(extract_keywords(keyword.strip()))

    if not extracted_keywords:
        raise ValueError("No valid keywords provided.")

    combined_keywords = " ".join(set(extracted_keywords + keyword_list))

    vectorizer = TfidfVectorizer()
    texts = [r.get("title", "") + " " + r.get("snippet", "") for r in results]

    try:
        if not any(text.strip() for text in texts):
            return results
            
        all_texts = texts + [combined_keywords]
        
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        query_vector = tfidf_matrix[-1:]
        result_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(result_vectors, query_vector).flatten()
        
        ranked_results = sorted(zip(results, similarities), key=lambda x: x[1], reverse=True)
        return [r[0] for r in ranked_results]
    except Exception as e:
        print(f"Error in TF-IDF processing: {e}")
        return results
