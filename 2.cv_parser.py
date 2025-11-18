import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

INPUT_FOLDER = "json_raw_text_in_progress/"
OUTPUT_FOLDER = "json_structured/"

GPT_MODEL = "gpt-5-mini" 

TARGET_SCHEMA = {
    "basic_detail": {
        "first_name": "", "last_name": "", "middle_names": "", "date_of_birth": "", "gender": "", "image": ""
    },
    "career_details": {
        "role": "", "career_summary": ""
    },
    "contact_details": {
        "phones": [], "emails": [], 
        "address": {"line1": "", "line2": "", "city": "", "zip_code": "", "country": ""},
        "urls": {"self": "", "linkedin": "", "github": ""}
    },
    "areas_of_expertise": [{"title": "", "subskills": []}],
    "soft_skills": [],
    "work_experience": [{
        "role": "", "company": "", "country": "", "type": "", "start_date": "", "end_date": "", "description": []
    }],
    "education": [{
        "programme": "", "institution": "", "city": "", "country": "", "start_date": "", "end_date": "", "class": "", "description": ""
    }],
    "hobbies": [],
    "references": {"available_upon_request": True, "people": []},
    "languages": [{"language": "", "description": []}],
    "awards": [], "publications": [], "patents": [], "books": [], "book_chapters": [], 
    "conferences": [], "technical_reports": [], "white_papers": [], "online_articles": [],
    "projects": [{"role": "", "title": "", "description": "", "url": ""}],
    "certifications": [],
    "committees_and_memberships": [{"role": "", "organisation": ""}],
    "other_files": [{"title": "", "file_url": ""}]
}

def parse_cv_with_gpt4(cv_text: str, client: openai.OpenAI) -> dict | None:
    """Sends CV text to the GPT model for structured information extraction."""
    
    system_prompt = (
        "You are an expert CV/Resume Parser. Your sole function is to extract all named entities and "
        "information from the user-provided raw CV text and format the output STRICTLY into the JSON schema provided. "
        "Rules to Follow: 1. Only include data explicitly found in the text. DO NOT make up information. "
        "2. If a field's data is not present in the CV text, set its value to an empty string (\"\") or an empty array/list ([]), "
        "maintaining the exact structure and keys. 3. Output MUST be valid JSON, using the provided schema as a template."
    )

    user_prompt = f"""
    Please extract the information from the following CV text and return it as a JSON object:

    --- CV TEXT START ---
    {cv_text}
    --- CV TEXT END ---

    The target JSON structure is:
    {json.dumps(TARGET_SCHEMA, indent=2)}
    """

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        parsed_data = json.loads(response.choices[0].message.content)
        return parsed_data
    
    except openai.APIError as e:
        print(f"\n[API ERROR] Skipping file due to API error: {e}")
        return None
    except json.JSONDecodeError:
        print("\n[JSON DECODE ERROR] Model returned malformed JSON.")
        return None

if __name__ == "__main__":
    try:
        client = openai.OpenAI()
        print("OpenAI client initialized.")
    except Exception:
        print("FATAL ERROR: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        exit()

    if not os.path.exists(OUTPUT_FOLDER):
        print(f"Creating output directory: {OUTPUT_FOLDER}")
        os.makedirs(OUTPUT_FOLDER)

    try:
        input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".json")]
        if not input_files:
            print(f"No JSON files found in {INPUT_FOLDER}. Please check the folder path.")
            exit()
        print(f"Found {len(input_files)} files to process in {INPUT_FOLDER}.")
    except FileNotFoundError:
        print(f"FATAL ERROR: Input directory '{INPUT_FOLDER}' not found.")
        exit()

    for i, input_filename in enumerate(input_files):
        print(f"\nProcessing file {i+1}/{len(input_files)}: {input_filename}...")
        
        input_filepath = os.path.join(INPUT_FOLDER, input_filename)
        output_filepath = os.path.join(OUTPUT_FOLDER, input_filename)

        if os.path.exists(output_filepath):
            print(f"Skipping {input_filename}: Output already exists.")
            continue
            
        try:
            with open(input_filepath, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            cv_text = raw_data.get('text', '')
            if not cv_text:
                print(f"Skipping {input_filename}: 'text' field is empty.")
                continue

        except Exception as e:
            print(f"Error reading or decoding {input_filename}: {e}")
            continue

        parsed_cv_data = parse_cv_with_gpt4(cv_text, client)

        if parsed_cv_data:
            try:
                with open(output_filepath, "w", encoding="utf-8") as f:
                    json.dump(parsed_cv_data, f, ensure_ascii=False, indent=2)
                print(f"--- SUCCESSFULLY PARSED AND SAVED: {input_filename} ---")
            except Exception as e:
                print(f"Error saving {input_filename}: {e}")

    print("\nBatch processing complete.")