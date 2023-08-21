import os
from pdf2image import convert_from_path
import pytesseract
import argparse
from multiprocessing import Pool
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

# Quality Improvement: Preprocessing function
def preprocess_image(image, desired_size=(1440, 1920)):
    # Convert PIL Image to OpenCV format for some operations
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Image Rotation (if needed):
    try:
        rotate_degree = pytesseract.image_to_osd(image_cv).split("\n")[1].split(":")[1].strip()
        image = image.rotate(float(rotate_degree))
    except:
        pass

    # Adaptive Binarization:
    image_cv_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    image_cv_bin = cv2.adaptiveThreshold(image_cv_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    image = Image.fromarray(image_cv_bin)

    # Noise removal
    image = image.filter(ImageFilter.MedianFilter())

    # Resize and Padding:
    image.thumbnail(desired_size, Image.LANCZOS)
    new_img = Image.new("L", desired_size, "white")
    new_img.paste(image, ((desired_size[0]-image.width)//2, (desired_size[1]-image.height)//2))
    image = new_img

    return image

def extract_text_from_image(image):
    try:
        # Preprocessing the image
        processed_image = preprocess_image(image)
        return pytesseract.image_to_string(processed_image, lang='eng')
    except Exception as e:
        print(f"Error during OCR: {str(e)}")
        return ""

def extract_text_from_pdf(file_path):
    try:
        images = convert_from_path(file_path)
    except Exception as e:
        print(f"Error during PDF-to-image conversion: {str(e)}")
        return ""

    # Performance: Using multiprocessing for concurrent OCR processing
    with Pool() as pool:
        texts = pool.map(extract_text_from_image, images)
    
    # Adding "Page X start" and "Page X end" between the pages
    for i in range(len(texts)):
        texts[i] = f"Page {i+1} start\n" + texts[i] + f"\nPage {i+1} end\n"

    return "".join(texts)

def save_to_txt(output_folder, filename, text):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.splitext(os.path.join(output_folder, filename))[0] + '.txt'
    
    # File Handling: Check if the output file already exists
    if os.path.exists(output_path):
        print(f"File {output_path} already exists. Skipping...")
        return

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main(data_folder, output_folder, desired_pdf=None):
    if not desired_pdf:
        pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
    else:
        pdf_files = [desired_pdf]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_folder, pdf_file)
        if os.path.exists(pdf_path):
            # Check if the file was already processed
            output_file_path = os.path.splitext(os.path.join(output_folder, pdf_file))[0] + '.txt'
            if os.path.exists(output_file_path):
                print(f"File {pdf_file} was already processed. Skipping...")
                continue

            print(f"Processing file: {pdf_file}")
            extracted_text = extract_text_from_pdf(pdf_path)
            save_to_txt(output_folder, pdf_file, extracted_text)
        else:
            print(f"File {pdf_file} not found in {data_folder}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process PDFs using OCR.')
    parser.add_argument('--data_folder', default='./pdfs_1077', help='Directory containing PDFs')
    parser.add_argument('--output_folder', default='ocrs', help='Directory to save output text files')
    parser.add_argument('--pdf', default=None, help='Specific PDF file to process')
    args = parser.parse_args()

    main(args.data_folder, args.output_folder, args.pdf)
