# app.py
import streamlit as st
import pandas as pd
from model import get_similarity
from utils import extract_text_from_pdf, extract_text_from_docx, extract_skills

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("### 👋 About the App")
    st.markdown("AI Resume Matcher built with SentenceTransformers and Streamlit.")
    st.markdown("### 📬 Connect")
    st.markdown("[LinkedIn](https://linkedin.com/in/sachingupta-ds) | [GitHub](https://github.com/Sachin-Kumar-Gupta)")

# -------------------------------
# Main App
# -------------------------------
st.title("🤖 AI Resume & Job Description Matcher")

col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader("📄 Upload your Resume", type=["pdf", "docx"])
with col2:
    job_descriptions_input = st.text_area(
        "Paste Job Descriptions (separate by blank lines):",
        height=250
    )

if st.button("🔍 Find Matches"):
    if uploaded_file and job_descriptions_input.strip():
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        resume_skills = extract_skills(resume_text)
        job_descriptions = [jd.strip() for jd in job_descriptions_input.split("\n\n") if jd.strip()]

        results, skill_gaps = [], []
        for jd in job_descriptions:
            score = get_similarity(resume_text, jd)
            jd_skills = extract_skills(jd)
            missing = jd_skills - resume_skills
            results.append((jd[:100] + "...", score))
            skill_gaps.append(", ".join(missing) if missing else "✔️ All key skills present")

        df = pd.DataFrame({
            "Job Description (preview)": [r[0] for r in results],
            "Match %": [r[1] for r in results],
            "Missing Skills": skill_gaps
        }).sort_values("Match %", ascending=False)

        st.success("✅ Matching Complete!")
        st.bar_chart(df.set_index("Job Description (preview)")["Match %"])
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", data=csv, file_name='results.csv')

    else:
        st.warning("Please upload a resume and paste job descriptions.")
