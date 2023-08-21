import os
import json
import shutil
import pandas as pd

# Directory containing the images
# image_dir = 'images_1280_1600'
image_dir = 'images_1920_2560'

# Directory containing the metadata.jsonl
metadata_dir = 'metadata'

# Directory where the train, validation, and test sets will be saved
# dataset_dir = 'dataset_1280_1600'
dataset_dir = 'dataset_1920_2560'

# Load the metadata
with open(os.path.join(metadata_dir, 'metadata.jsonl'), 'r') as f:
    metadata = [json.loads(line) for line in f]

# Convert the metadata to a DataFrame
df = pd.DataFrame(metadata)

# Load the sampled filenames
train_files_df = pd.read_csv(os.path.join(metadata_dir, 'train_files.csv'))
val_files_df = pd.read_csv(os.path.join(metadata_dir, 'val_files.csv'))
test_files_df = pd.read_csv(os.path.join(metadata_dir, 'test_files.csv'))

train_files = train_files_df.values.flatten()
val_files = val_files_df.values.flatten()
test_files = test_files_df.values.flatten()

# Filter the metadata DataFrame based on the loaded filenames
train_df = df[df['file_name'].isin(train_files)]
val_df = df[df['file_name'].isin(val_files)]
test_df = df[df['file_name'].isin(test_files)]

# Create directories for the training, validation, and test sets
for subset in ['train', 'validation', 'test']:
    os.makedirs(os.path.join(dataset_dir, subset), exist_ok=True)

# Function to save a subset of the data
def save_subset(df, subset):
    # Save the images
    for _, row in df.iterrows():
        shutil.copy(os.path.join(image_dir, row['file_name']),
                    os.path.join(dataset_dir, subset, row['file_name']))
    # Save the metadata
    with open(os.path.join(dataset_dir, subset, 'metadata.jsonl'), 'w') as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict()) + '\n')
    print(f"Number of images in {subset}: {len(df)}")

# Save the training, validation, and test sets
save_subset(train_df, 'train')
save_subset(val_df, 'validation')
save_subset(test_df, 'test')

# Print the images that were not touched
untouched_images = [image for image in os.listdir(image_dir) if image not in df['file_name'].values]
print(f"Number of untouched images: {len(untouched_images)}")
for image in untouched_images:
    print(f"Untouched image: {image}")
