import os
import json

# Directory paths
gpt_4_outputs_dir = "gpt_4_outputs"
metadata_dir = "metadata"

# File paths
metadata_file = os.path.join(metadata_dir, 'metadata.jsonl')
merged_file = os.path.join(metadata_dir, 'merged_gpt4.jsonl')

# Load metadata
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata = [json.loads(line) for line in f]

print(f"Loaded {len(metadata)} entries from metadata.jsonl")

# Function to check if two entries match based on the file name
def entries_match(entry1, entry2):
    adjusted_file_name = entry1['file_name'].replace('.txt', '.jpg')
    return adjusted_file_name == entry2['file_name']

# List to store problematic files
error_files = []
not_found_files = []
duplicates = []

# Set to track processed files
processed_files = set()

# Process each JSON file in the gpt_4_outputs directory
with open(merged_file, 'w', encoding='utf-8') as out_f:
    for filename in os.listdir(gpt_4_outputs_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(gpt_4_outputs_dir, filename)
            print(f"Processing: {filename}")
            
            # Check for duplicates
            if filename in processed_files:
                duplicates.append(filename)
                continue
            processed_files.add(filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Replace special character ” with standard "
                data_str = json.dumps(data).replace('”', '"')
                data = json.loads(data_str)
                
                # Convert vendor_name to lowercase in predictions
                if "vendor_name" in data["gpt_4_predictions"]:
                    data["gpt_4_predictions"]["vendor_name"] = data["gpt_4_predictions"]["vendor_name"].lower()
                
                # Look for matching metadata entries
                matches = [meta for meta in metadata if entries_match(data, meta)]

                if matches:
                    ground_truth = json.loads(matches[0]['ground_truth'])['gt_parse']
                    if "vendor_name" in ground_truth:
                        ground_truth["vendor_name"] = ground_truth["vendor_name"].lower()
                        if ground_truth["vendor_name"] in data["gpt_4_predictions"]["vendor_name"]:
                            data["gpt_4_predictions"]["vendor_name"] = ground_truth["vendor_name"]
                    
                    # Merge the metadata with the prediction
                    matched_entry = {
                        "file_name": data["file_name"].replace('.txt', '.jpg'),
                        "ground_truth": json.dumps(ground_truth),
                        "predictions": json.dumps(data['gpt_4_predictions'])
                    }

                    # Write the matched entry to the merged file
                    out_f.write(json.dumps(matched_entry) + '\n')
                    print(f"Matched and wrote entry for: {filename}")
                else:
                    print(f"No match found for: {filename}")
                    not_found_files.append(filename)
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                error_files.append(filename)

# Summary
if not error_files and not duplicates and not not_found_files:
    print("All files were processed successfully!")
else:
    if error_files:
        print(f"Errors occurred while processing {len(error_files)} files.")
        for err_file in error_files:
            print(f"- {err_file}")
    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate files.")
        for dup_file in duplicates:
            print(f"- {dup_file}")
    if not_found_files:
        print(f"\nNo matches found for {len(not_found_files)} files.")
        for nf_file in not_found_files:
            print(f"- {nf_file}")
