"""
Resume Ranking Engine
---------------------
Uses TF-IDF vectorisation + cosine similarity to rank
applicants against a job description.

Algorithm:
  1. Build a corpus: [job_description] + [resume_1_text, resume_2_text, ...]
  2. Fit TF-IDF vectoriser on the entire corpus
  3. Transform each document into a TF-IDF vector
  4. Compute cosine similarity between job vector and each resume vector
  5. Return scores in descending order
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def rank_resumes(job_description: str, resumes: list) -> list:
    """
    Rank resumes against a job description using TF-IDF cosine similarity.

    Parameters
    ----------
    job_description : str
        Full text of the job posting (title + description + requirements).
    resumes : list of dict
        Each dict must have:
            'id'   : application or resume identifier
            'text' : extracted resume text

    Returns
    -------
    list of dict, sorted by score descending
        [{'id': ..., 'score': float (0.0–1.0)}, ...]
    """
    if not resumes:
        return []

    # Filter out entries with no text to avoid empty-vector errors
    valid_resumes = [r for r in resumes if r.get('text', '').strip()]
    if not valid_resumes:
        return [{'id': r['id'], 'score': 0.0} for r in resumes]

    # Build corpus: job description first, then each resume
    corpus = [job_description] + [r['text'] for r in valid_resumes]

    # TF-IDF with English stop-word removal and character n-grams for robustness
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),   # unigrams + bigrams capture phrases like "machine learning"
        max_features=10000,
        sublinear_tf=True,    # apply log normalisation to term frequencies
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError as e:
        print(f"[ranking] TF-IDF error: {e}")
        return [{'id': r['id'], 'score': 0.0} for r in resumes]

    # Job vector is the first row; resume vectors follow
    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    # Cosine similarities → flat array
    similarities = cosine_similarity(job_vector, resume_vectors).flatten()

    # Map back to original ids
    results = []
    for idx, resume in enumerate(valid_resumes):
        score = float(np.clip(similarities[idx], 0.0, 1.0))
        results.append({'id': resume['id'], 'score': round(score, 4)})

    # Include resumes that had no text with score 0
    valid_ids = {r['id'] for r in valid_resumes}
    for r in resumes:
        if r['id'] not in valid_ids:
            results.append({'id': r['id'], 'score': 0.0})

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def build_job_corpus_text(job) -> str:
    """Helper: concatenate all relevant job fields into one string for vectorisation."""
    parts = [
        job.title or '',
        job.company or '',
        job.description or '',
        job.requirements or '',
        job.skills_required or '',
    ]
    return ' '.join(parts)
