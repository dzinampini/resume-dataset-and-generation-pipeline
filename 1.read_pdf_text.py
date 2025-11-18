import os
import json
import pdfplumber
import pytesseract
from PIL import Image
from tqdm import tqdm

PDF_FOLDER = "pdfs/"                
OUTPUT_FOLDER = "json_raw_text/"           
USE_OCR_IF_EMPTY = True             
MAX_PAGES_OCR = 2                    
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_text_pdfplumber(pdf_path):
    """Extract text using pdfplumber. Returns empty string if extraction fails."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text.append(page_text)
            return "\n".join(text).strip()
    except:
        return ""



def extract_text_ocr(pdf_path, max_pages=2):
    """OCR the first N pages of a PDF using Tesseract."""
    try:
        import fitz
    except ImportError:
        print("Please install: pip install pymupdf")
        return ""

    text = []
    pdf = fitz.open(pdf_path)

    pages_to_ocr = min(max_pages, pdf.page_count)

    for i in range(pages_to_ocr):
        page = pdf.load_page(i)
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        page_text = pytesseract.image_to_string(img)
        text.append(page_text)

    return "\n".join(text).strip()


def convert_pdfs():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDF files.")
    for pdf_file in tqdm(pdf_files, desc="Converting PDFs"):
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)

        text = extract_text_pdfplumber(pdf_path)

        if USE_OCR_IF_EMPTY and len(text.strip()) < 20:
            text = extract_text_ocr(pdf_path, max_pages=MAX_PAGES_OCR)

        ls_item = {
            "document_id": pdf_file.replace(".pdf", ""),
            "filename": pdf_file,
            "text": text
        }

        out_path = os.path.join(
            OUTPUT_FOLDER,
            pdf_file.replace(".pdf", ".json")
        )

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(ls_item, f, indent=2, ensure_ascii=False)

    print("Conversion complete!")
    print(f"JSON files saved in: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    convert_pdfs()
