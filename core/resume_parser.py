# Code to extract text from PDF resumes
import fitz  # PyMuPDF

def extract_resume_text(pdf_path):
    """
    Extracts all text from a PDF resume.
    
    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text from all pages
    """
    text = ""

    # Open the PDF using PyMuPDF
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()  # Extract text from each page

    return text
