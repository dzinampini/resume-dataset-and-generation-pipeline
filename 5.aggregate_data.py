import os
import json

INPUT_DIR = 'json_merged'
OUTPUT_FILE = 'all_merged_data_array.json'

def aggregate_json_files():
    """
    Reads all JSON files from the input directory and combines them into a single 
    JSON array saved in the output file.
    """
    all_data = []
    file_count = 0
    
    print(f"Starting aggregation process from directory: '{INPUT_DIR}'")

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.json') and os.path.isfile(os.path.join(INPUT_DIR, filename)):
            filepath = os.path.join(INPUT_DIR, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data_item = json.load(f)
                
                all_data.append(data_item)
                file_count += 1
                
            except json.JSONDecodeError:
                print(f"Error: Skipping file '{filename}'. Failed to decode JSON.")
            except Exception as e:
                print(f"An unexpected error occurred with '{filename}': {e}")
    
    print(f"\nSuccessfully read {file_count} JSON objects.")
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            json.dump(all_data, outfile, indent=2)
        
        print(f"Aggregation complete! The final array of {len(all_data)} items is saved to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"Critical Error: Could not write output file '{OUTPUT_FILE}': {e}")

if __name__ == "__main__":
    aggregate_json_files()