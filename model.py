# model.py
from sentence_transformers import SentenceTransformer, util

# Load model only once (global)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity(resume_text, jd_text):
    """Compute cosine similarity score between resume and job description."""
    res_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    score = util.cos_sim(res_emb, jd_emb).item() * 100
    return round(score, 2)
