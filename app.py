# app.py
import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, get_match_score

# ========================================================
# PAGE CONFIGURATION
# ========================================================
st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("🤖 AI Resume Matcher")
st.caption("Match your resume skills with job descriptions instantly!")

# ========================================================
# SESSION STATE INITIALIZATION
# ========================================================
if "results" not in st.session_state:
    st.session_state.results = []   # store JD-wise match history

# ========================================================
# SIDEBAR - RESUME UPLOAD
# ========================================================
with st.sidebar:
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type == "pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("❌ Please upload only PDF or DOCX files.")
            st.stop()

        extracted_skills = extract_skills(resume_text)
        st.success(f"✅ Resume uploaded successfully!")
        st.markdown(f"**Extracted Skills:** {', '.join(extracted_skills)}")
    else:
        st.warning("⚠️ Please upload your resume to start matching.")
        resume_text = ""

# ========================================================
# MAIN SECTION - JOB DESCRIPTION INPUT
# ========================================================
st.markdown("### 🧾 Paste a Job Description Below")
job_description = st.text_area(
    "Paste one complete job description here:",
    placeholder="Copy and paste the full JD...",
    height=250
)

# ========================================================
# MATCHING LOGIC
# ========================================================
if st.button("🔍 Check Match"):
    if uploaded_file and job_description.strip():
        # get match score for one JD
        job_df = get_match_score(resume_text, [job_description])
        jd_title = job_df.iloc[0]['Job Description'][:60] + "..."  # short preview
        score = round(job_df.iloc[0]['Match Score (%)'], 2)
        skills = job_df.iloc[0]['Missing Skills']

        # Append to session state results
        st.session_state.results.append({
            "Job Description": jd_title,
            "Match Score (%)": score,
            "Missing Skills": skills
        })
        st.success(f"✅ Match calculated! (Score: {score}%)")
    else:
        st.warning("⚠️ Please upload your resume and enter a job description first.")

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
