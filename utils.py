# utils.py
import fitz  # PyMuPDF
import docx
import re

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    skills = re.findall(r'\b(python|sql|power\s*bi|excel|tableau|ml|machine learning|nlp|tensorflow|pandas|numpy|spacy|keras|flask)\b', text.lower())
    return set(skills)
