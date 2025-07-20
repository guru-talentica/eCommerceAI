import PyPDF2
import sys

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        return text

if __name__ == "__main__":
    pdf_path = "Backend - First Assignment.pdf"
    extracted_text = extract_pdf_text(pdf_path)
    print(extracted_text)
