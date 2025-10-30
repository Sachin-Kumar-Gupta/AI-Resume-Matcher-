# utils.py
# utils.py

from PyPDF2 import PdfReader
import docx
import re


# ==============================
# 1️⃣ Extract text from PDF
# ==============================
def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


# ==============================
# 2️⃣ Extract text from DOCX
# ==============================
def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


# ==============================
# 3️⃣ Clean and preprocess text
# ==============================
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # remove multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ASCII chars
    return text.strip()


# ==============================
# 4️⃣ Handle file upload and extraction
# ==============================
def extract_resume_text(uploaded_file):
    """
    Detect file type and extract text accordingly.
    """
    file_type = uploaded_file.name.split('.')[-1].lower()
    temp_path = f"temp_resume.{file_type}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text based on file type
    if file_type == "pdf":
        text = extract_text_from_pdf(temp_path)
    elif file_type in ["docx", "doc"]:
        text = extract_text_from_docx(temp_path)
    else:
        return None

    return clean_text(text)
