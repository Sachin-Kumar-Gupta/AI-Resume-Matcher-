# utils.py
from PyPDF2 import PdfReader
import docx
import re

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    skills = re.findall(r'\b(python|sql|power\s*bi|excel|tableau|ml|machine learning|nlp|tensorflow|pandas|numpy|spacy|keras|flask)\b', text.lower())
    return set(skills)

