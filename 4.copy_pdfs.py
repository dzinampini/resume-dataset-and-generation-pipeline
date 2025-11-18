import os
import shutil
import glob

JSON_DIR = 'json_merged'
SOURCE_PDF_DIR = 'pdfs'
TARGET_PDF_DIR = os.path.join(JSON_DIR, 'pdfs')

def copy_matching_pdfs():
    os.makedirs(TARGET_PDF_DIR, exist_ok=True)
    
    print(f"Starting PDF matching and copy process...")
    print(f"Source PDF directory: '{SOURCE_PDF_DIR}'")
    print(f"Target PDF directory: '{TARGET_PDF_DIR}'\n")

    for json_filename in os.listdir(JSON_DIR):
        if json_filename.endswith('.json'):
        
            pdf_filename = json_filename.replace('.json', '.pdf') 
            
            source_pdf_path = os.path.join(SOURCE_PDF_DIR, pdf_filename)
            target_pdf_path = os.path.join(TARGET_PDF_DIR, pdf_filename)

            if os.path.exists(source_pdf_path):
                try:
                    shutil.copy2(source_pdf_path, target_pdf_path)
                    print(f"Copied: {pdf_filename}")
                except Exception as e:
                    print(f"Error copying {pdf_filename}: {e}")
            else:
                print(f"PDF not found for JSON '{json_filename}' at: {source_pdf_path}. Skipping.")

    print("\nProcessing complete! Matching PDFs are now in 'json_merged/pdfs'.")

if __name__ == "__main__":
    copy_matching_pdfs()