# utils.py
from PyPDF2 import PdfReader
import re
import docx
import pandas as pd
from transformers import pipeline

# 1️⃣ PDF & DOCX TEXT EXTRACTION

def extract_text_from_pdf(uploaded_file):
    """Extracts text from uploaded PDF."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(uploaded_file):
    """Extracts text from uploaded DOCX."""
    doc = docx.Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# SKILL EXTRACTION (from Resume Text)

def extract_skills(resume_text):
    """Extracts relevant skills from resume text using regex-based matching."""
    skill_keywords = [
        "python", "sql", "tableau", "power bi", "excel", "numpy", "pandas", "matplotlib",
        "seaborn", "tensorflow", "pytorch", "scikit-learn", "ml", "machine learning",
        "deep learning", "nlp", "natural language processing", "llm", "transformers",
        "data analysis", "data visualization", "statistics", "communication", "r",
        "predictive modeling", "time series", "feature engineering"
    ]

    resume_text = resume_text.lower()
    found_skills = [skill for skill in skill_keywords if skill in resume_text]
    return list(set(found_skills))

# MATCH SCORE GENERATOR

def get_match_score(resume_text, job_descriptions):
    """Compares resume with each job description using transformer model."""
    
    # Load model (you can replace with more advanced one if needed)
    model = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

    resume_features = model(resume_text)
    
    results = []
    for jd in job_descriptions:
        jd_features = model(jd)

        # Mean pooling
        resume_vec = sum(resume_features[0][0]) / len(resume_features[0][0])
        jd_vec = sum(jd_features[0][0]) / len(jd_features[0][0])

        # Cosine similarity
        similarity = cosine_similarity(resume_vec, jd_vec)
        match_score = similarity * 100

        # Missing skills check
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd)
        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

        results.append({
            "Job Description": jd.strip()[:100],
            "Match Score (%)": round(match_score, 2),
            "Missing Skills": "✔️ All key skills present" if not missing_skills else ", ".join(missing_skills)
        })
    
    return pd.DataFrame(results)

# HELPER FUNCTION — COSINE SIMILARITY

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two embeddings."""
    import numpy as np
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
