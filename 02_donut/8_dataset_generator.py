from pathlib import Path
import random
from datasets import load_dataset
import os

# First do this in the terminal:
# huggingface-cli login

class DonutDatasetGenerator:
    def generate(self, data_dir):
        print("Starting generate method") 
        # define paths
        img_dir_path = Path(data_dir)

        # Load dataset
        dataset = load_dataset("imagefolder", data_dir=img_dir_path, split="train")

        print(f"Dataset has {len(dataset)} images")
        print(f"Dataset features are: {dataset.features.keys()}")

        random_sample = random.randint(0, len(dataset) - 1)
        print(f"Random sample is {random_sample}")
        print(f"Ground truth text is {dataset[random_sample]['ground_truth']}")
        print("Finished generate method")

class DonutDatasetUploader:
    def upload(self, data_dir, dataset_name):
        # define paths
        img_dir_path = Path(data_dir)

        dataset = load_dataset("imagefolder", data_dir=img_dir_path)

        # Save dataset: https://huggingface.co/docs/datasets/main/en/image_dataset
        dataset.push_to_hub("onlas/dataset_1920_2560", private=True) # attention

class DonutDatasetTester:
    def test(self, dataset_name):
        # Load dataset
        dataset = load_dataset(dataset_name, split="train")

        print(f"Dataset has {len(dataset)} images")
        print(f"Dataset features are: {dataset.features.keys()}")

        random_sample = random.randint(0, len(dataset) - 1)
        print(f"Random sample is {random_sample}")
        print(f"Ground truth is {dataset[random_sample]['ground_truth']}")

def main():
    # Define the path to your dataset and the name you want to give it on the Datasets Hub
    data_dir = "dataset_1920_2560" # attention
    dataset_name = "dataset_1920_2560" # attention

    # Create an instance of DonutDatasetGenerator and use it to generate your dataset
    dataset_generator = DonutDatasetGenerator()
    dataset_generator.generate(data_dir)

    # Create an instance of DonutDatasetUploader and use it to upload your dataset to the Datasets Hub
    dataset_uploader = DonutDatasetUploader()
    dataset_uploader.upload(data_dir, dataset_name)

    # Create an instance of DonutDatasetTester and use it to test your dataset
    dataset_tester = DonutDatasetTester()
    dataset_tester.test("onlas/dataset_1920_2560") # attention

if __name__ == "__main__":
    main()