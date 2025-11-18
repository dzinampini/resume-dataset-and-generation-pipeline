# Resume Dataset Generation Pipeline
This repository documents a complete workflow for enhancing and structuring resume data. It starts with raw PDF files (specifically a subset of the Annotated NER PDF Resumes dataset) and generates a highly detailed, machine-readable JSON array suitable for advanced data analysis or machine learning applications.

The pdf files were obtained from [Mehyaar/Annotated_NER_PDF_Resumes](https://huggingface.co/datasets/Mehyaar/Annotated_NER_PDF_Resumes/tree/main) This process was used to create a structured dataset of only 939 resumes from this dataset. 

## Option 1: Just get the final dataset
For users who only require the final output, the complete dataset is available here:
full_dataset.json: A single JSON array containing all 939 structured records.

## Option 2: Running the dataset generation pipeline on your own 
To successfully run this entire pipeline, you must install the necessary software and set up your Python environment.

1. System Requirements
Tesseract OCR: Required for reliable text extraction from image-based PDFs (used in Step 1). 
OpenAI API Key: Required for the Large Language Model (LLM) parsing in Step 2.

2. Python Environment Setup
Install all necessary libraries using the following command:
```bash
pip install pdfplumber pytesseract Pillow tqdm openai python-dotenv pymupdf shutil
```

3. Project Structure
Before starting, ensure you have added the following files in your main directory
.env        <-- Contains OPENAI_API_KEY="sk-..."
pdfs/       <-- INPUT: Place all your source PDF resumes here


### The 5-Step Data Processing Pipeline
The scripts must be run in the numerical order listed below.
#### Step 1: Extract Raw Text from PDFs
```bash
python 1.read_pdf_text.py 
```

This script iterates through the /pdfs directory, extracts the raw text from each PDF, and saves it as a JSON file containing the document ID, filename, and raw text. It includes a fallback to Tesseract OCR for poorly structured or image-based PDFs.


##### Prepares the data for the next step:
```bash
mv json_raw_text json_raw_text_in_progress
```

#### Step 2: Parse Text into Structured JSON using an LLM
```bash
python 2.cv_parser.py
```
This script sends the raw text content to an LLM (specified in the script, using GPT-5 Mini) to be parsed into the specific, detailed TARGET_SCHEMA. This is the most time-consuming and costly step.

#### Prepares the data for the merge step:
```bash
mv json_raw_text_in_progress json_raw_text_done 
```
*Customization Note:* If you wish to change the structured output fields, modify the TARGET_SCHEMA variable within 2.cv_parser.py.

#### Step 3: Merge Raw and Structured JSON
```bash
python 3.merge_json_files.py
```
This script takes the two sets of JSON files—the raw text data (from Step 1) and the structured output (from Step 2)—and merges them into a single, comprehensive JSON file for each resume.

#### Step 4: Organize and Copy Matching PDFs
```bash
python 4.copy_pdfs.py
```
This is an organizational step. It checks the /pdfs folder for the original document corresponding to each merged JSON file and copies the PDF into a dedicated sub-folder within the merged directory.

#### Step 5: Aggregate All JSON Files
```bash
python 5.aggregate_data.py
```
The final step collects all the individual merged files into a single, cohesive file that is structured as a JSON array you can now use in your experiments.

## Cite this Work
C. Chipfumbu, M. Giyane, D. Mpini, T. Dumani, and C. Magidi, "Resume Dataset with Generation Pipeline". Zenodo, Nov. 18, 2025. doi: 10.5281/zenodo.17639095.
