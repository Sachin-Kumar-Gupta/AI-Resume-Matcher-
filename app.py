# app.py
# app.py

import streamlit as st
from model import get_similarity
from utils import extract_resume_text
import os

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Matcher")
st.write("Easily compare your resume with any job description using NLP & Hugging Face embeddings.")

# ==============================
# SESSION STATE
# ==============================
if "history" not in st.session_state:
    st.session_state["history"] = []


# ==============================
# FILE UPLOAD
# ==============================
st.subheader("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"],
    help="Upload your resume to analyze and match it with job descriptions."
)

if uploaded_file:
    resume_text = extract_resume_text(uploaded_file)
    if not resume_text:
        st.error("⚠️ Could not extract text from this file. Please upload a clear PDF or DOCX.")
    else:
        st.success("✅ Resume uploaded and extracted successfully!")

        # ==============================
        # JOB DESCRIPTION INPUT
        # ==============================
        st.subheader("🧾 Paste Job Description")
        jd_text = st.text_area(
            "Paste the full job description here (only one JD at a time).",
            height=250,
            help="Copy and paste the job description from LinkedIn, Indeed, or any job portal."
        )

        # ==============================
        # MATCH BUTTON
        # ==============================
        if st.button("🔍 Analyze Match"):
            if jd_text.strip():
                score = calculate_similarity(resume_text, jd_text)
                
                # Save to history
                st.session_state["history"].append({
                    "jd": jd_text[:100] + "...",
                    "score": score
                })
                
                st.success(f"✅ Match Score: **{score}%**")
                
                # Score interpretation
                if score >= 80:
                    st.info("💪 Excellent match! You’re highly aligned with this role.")
                elif score >= 60:
                    st.warning("⚖️ Moderate match. You meet several requirements but can improve.")
                else:
                    st.error("❌ Weak match. Try tailoring your resume or picking another job.")
            else:
                st.warning("Please paste a job description before analyzing.")


# ========================================================
# DISPLAY RESULTS TABLE
# ========================================================
if st.session_state.results:
    st.subheader("📊 All Checked Job Matches")
    result_df = pd.DataFrame(st.session_state.results)
    st.dataframe(result_df, use_container_width=True)

    # Bar Chart
    st.bar_chart(result_df.set_index("Job Description")["Match Score (%)"])

    # Download Results Option
    csv_data = result_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name="resume_match_results.csv",
        mime="text/csv"
    )

# ==============================
# MATCH HISTORY
# ==============================
if st.session_state["history"]:
    st.subheader("🕒 Match History")
    for idx, record in enumerate(reversed(st.session_state["history"]), 1):
        st.write(f"**{idx}.** JD Snippet: {record['jd']} → **Score:** {record['score']}%")

# ========================================================
# RESET BUTTON
# =========================
if st.button("🗑️ Clear All Results"):
    st.session_state.results = []
    st.info("All previous match results cleared.")

# ========================================================
# FOOTER
# ========================================================
st.markdown("---")

st.caption("🚀 Built with ❤️ using Streamlit and Hugging Face Transformers by Sachin Kumar Gupta.")
