# Information Extraction from Invoices

## Objective

The project's primary aim is to extract structured information from invoices utilising Donut transformer models.

## 📂 Directory Overview

### 🔵 01_webapp

A Streamlit application for uploading and processing images or PDFs using the Donut model. Outputs can be saved in JSON or Excel format.

### 🔵 02_donut

Encompasses the main data processing scripts and associated resources.

- **Directories**:
  - `excels/`: For Excel files.
  - `metadata/`: Contains metadata formatted as .jsonl.
  - `pdfs_1077/`: Stores PDFs awaiting processing.
  
- **Python Scripts Overview**:
  1. `1_xlsx_to_jsonl_.py`: Transforms Excel files to the JSONL metadata format.
  2. `2_pdf_to_pic.py`: Converts PDFs into images at different resolutions.
  3. `3_check_sizes.py`: Offers insights into image dimensions.
  4. `4_padding.py`: Adjusts images below a certain size by adding padding.
  5. `5_create_stratas_for_dataset.py`: Facilitates stratified sampling based on vendor details.
  6. `6_prepare_data.py`: Categorises images into train, validation, or test groups.
  7. `7_remove_hf_dataset.py`: Deletes datasets from a Hugging Face repository.
  8. `8_dataset_generator.py`: Includes classes like DonutDatasetGenerator (provides image details), DonutDatasetUploader (uploads datasets to HuggingFace), and DonutDatasetTester (tests and provides details of dataset samples).

### 🔵 03_gpt

Primarily related to GPT-based operations.

#### Directories:

- `excels/`: Holds the initial Excel datasets.
- `final_results/`: Consists of the processed results.
  - `_template/`: Sub-folders include:
    - `csv`: Where CSV files are stored.
    - `images`: For images related to results.
    - `merged_jsonl`: Contains merged results in JSONL format.
    - `report`: Likely for generated reports.
    - `results_json`: Holds processed results in JSON format.
- Additional directories include:
  - `gpt_3.5_outputs`: Contains GPT-3.5 outputs.
  - `gpt_4_outputs`: Contains GPT-4 outputs.
  - `images`: Contains images derived from various sources like PDFs.
  - `metadata`: Contains metadata about the datasets.
  - `ocrs`: Contains OCR outputs from scanned invoices.
  - `pdfs_1077`: Contains the PDFs ready for processing.

#### Scripts Overview:

1. `1_sort_out_pdfs.py`: Filters PDFs using metadata. Unmatched PDFs are segregated.
2. `2_xlsx_to_jsonl_.py`: Converts Excel invoice details to JSONL formatted metadata. Provides a summary of processed invoices.
3. `3_pdf_to_ocr_v03.py`: Focuses on OCR of PDFs. Steps include image preprocessing, using Tesseract for OCR, and other associated operations.
4. `4_gpt4_ocr_to_json_v04.py`: Converts OCR outputs to structured JSON using GPT-4. Manages various tasks like token counting, error handling, logging, and data saving.
5. `5_json_to_merged.jsonl_gpt4.py`: Merges GPT-4 outputs with metadata into a single file.

### 🔵 04_eda

Focuses on the Exploratory Data Analysis (EDA) of all contained data.

### 🔵 05_error_analysis

Geared towards setting up experiments (covering 36 experiments in total) and conducting error analysis. Contains:

1. `error_analysis_setup_12.ipynb` notebook to delve deep into GPT-4 output errors.
2. `Experiment_setup_12.ipynb` for conducting the experiments using GPU