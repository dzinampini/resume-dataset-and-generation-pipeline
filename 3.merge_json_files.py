import os
import json

RAW_TEXT_DIR = 'json_raw_text_done'
STRUCTURED_DIR = 'json_structured'
OUTPUT_DIR = 'json_merged'

def merge_json_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Starting merge process for files in '{RAW_TEXT_DIR}'...")

    for filename in os.listdir(RAW_TEXT_DIR):
        if filename.endswith('.json'):
            base_filename = filename 
            
            raw_text_path = os.path.join(RAW_TEXT_DIR, base_filename)
            structured_path = os.path.join(STRUCTURED_DIR, base_filename)
            output_path = os.path.join(OUTPUT_DIR, base_filename)

            if not os.path.exists(structured_path):
                print(f"Warning: Structured file not found for {base_filename}. Skipping.")
                continue

            try:
                with open(raw_text_path, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)

                with open(structured_path, 'r', encoding='utf-8') as f:
                    structured_data = json.load(f)

                merged_data = raw_data.copy()
                merged_data['structured_output'] = structured_data

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(merged_data, f, indent=4)
                
                print(f"Successfully merged and saved: {base_filename}")

            except json.JSONDecodeError:
                print(f"Error decoding JSON for file: {base_filename}. Skipping.")
            except Exception as e:
                print(f"An unexpected error occurred with {base_filename}: {e}")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    merge_json_files()