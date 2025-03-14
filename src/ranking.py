from sklearn.feature_extraction.text import TfidfVectorizer
from utils import extract_keywords


def rank_results(results, keyword, keyword_list):
    if not results:
        return []

    vectorizer = TfidfVectorizer()
    texts = [r.get("title", "") + " " + r.get("snippet", "") for r in results]

    if not keyword.strip():
        raise ValueError("Keyword cannot be empty.")

    extracted_keywords = extract_keywords(keyword.strip())
    combined_keywords = " ".join(extracted_keywords + keyword_list)

    try:
        tfidf_matrix = vectorizer.fit_transform(texts + [combined_keywords])
        cosine_similarities = (tfidf_matrix * tfidf_matrix.T).A[-1][:-1]
        ranked_results = sorted(zip(results, cosine_similarities), key=lambda x: x[1], reverse=True)
        return [r[0] for r in ranked_results]
    except ValueError as e:
        print(f"Error in TF-IDF processing: {e}")
        return results
