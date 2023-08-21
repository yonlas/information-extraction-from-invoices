import subprocess
import shutil
import os

# First do this in the terminal:
# huggingface-cli login

# Install necessary packages
subprocess.run(["pip", "install", "datasets"])
subprocess.run(["pip", "install", "huggingface_hub"])

# Clone the repository
subprocess.run(["git", "clone", "https://huggingface.co/datasets/onlas/dataset_1440_1920/"])

# Define the path to the 'dataset' directory in the cloned repository
dataset_dir = os.path.join("dataset_1440_1920", "data")

# Remove the 'dataset' directory if it exists
if os.path.exists(dataset_dir):
    shutil.rmtree(dataset_dir)

# Change working directory to the cloned repository
os.chdir("dataset_1440_1920")

# Commit the changes
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Remove 'dataset' directory"])

# Push the changes
subprocess.run(["git", "push"])

# Change back to the parent directory
os.chdir("..")

# Remove the cloned repository
os.system('rmdir /S /Q "{}"'.format("dataset_1440_1920"))


# onlas/dataset_1600_2048