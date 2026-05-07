"""
Resume parser utility.
Extracts raw text from PDF files using pdfplumber,
then identifies skills from a curated keyword list.
"""

import pdfplumber
import re
import os

# -----------------------------------------------------------------
# Comprehensive skill keyword dictionary used for extraction
# -----------------------------------------------------------------
SKILL_KEYWORDS = [
    # Programming languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby',
    'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab',
    # Web
    'html', 'css', 'react', 'angular', 'vue', 'node', 'nodejs', 'express',
    'django', 'flask', 'fastapi', 'spring', 'asp.net', 'laravel',
    # Databases
    'mysql', 'postgresql', 'sqlite', 'mongodb', 'redis', 'oracle',
    'cassandra', 'dynamodb', 'sql', 'nosql',
    # Data / ML
    'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch',
    'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'data analysis', 'data science', 'computer vision', 'neural network',
    # Cloud / DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
    'terraform', 'ansible', 'linux', 'bash', 'git', 'github', 'devops',
    # Soft / Other
    'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'excel',
    'powerpoint', 'project management', 'communication', 'leadership',
    'problem solving', 'teamwork',
]


def extract_text_from_pdf(filepath: str) -> str:
    """
    Open a PDF and concatenate text from every page.
    Returns empty string if extraction fails.
    """
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[resume_parser] Error reading PDF {filepath}: {e}")
    return text.strip()


def extract_skills(text: str) -> list:
    """
    Scan extracted text for known skill keywords (case-insensitive).
    Returns a deduplicated list of found skills.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = []

    for skill in SKILL_KEYWORDS:
        # Use word-boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)

    return list(dict.fromkeys(found))  # preserve order, deduplicate


def parse_resume(filepath: str) -> dict:
    """
    Main entry point.
    Returns dict with 'text' (full extracted text) and 'skills' (list).
    """
    text = extract_text_from_pdf(filepath)
    skills = extract_skills(text)
    return {
        'text': text,
        'skills': skills,
    }
