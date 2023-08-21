import os
import json

# Define the paths
metadata_path = 'metadata/metadata.jsonl'
pdfs_path = 'pdfs_1077'
not_found_path = os.path.join(pdfs_path, 'not found')

# Create 'not found' folder if it doesn't exist
if not os.path.exists(not_found_path):
    os.makedirs(not_found_path)

# Extract file names from metadata.jsonl
file_names = set()
with open(metadata_path, 'r') as f:
    for line in f:
        data = json.loads(line)
        file_name = data['file_name'].rsplit('.', 1)[0]  # Remove the extension
        file_names.add(file_name)

# Move unmatched PDFs to 'not found' folder
found_count = 0
not_found_count = 0
for file in os.listdir(pdfs_path):
    if file.endswith('.pdf'):
        file_name = file.rsplit('.', 1)[0]  # Remove the extension
        if file_name not in file_names:
            os.rename(os.path.join(pdfs_path, file), os.path.join(not_found_path, file))
            not_found_count += 1
        else:
            found_count += 1

# Print the results
print(f"{found_count} PDFs were found and left in the 'pdfs' folder.")
print(f"{not_found_count} PDFs were not found and moved to the 'not found' folder in the 'pdfs' folder.")

