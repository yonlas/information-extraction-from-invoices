from pdf2image import convert_from_path
import os
from PIL import Image
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_pdf_to_image(pdf_path, output_folder, output_size=(1920, 2560)): # attention
    # Check if the file is a PDF (case-insensitive)
    if pdf_path.lower().endswith('.pdf'):
        try:
            # Convert the first page of the PDF to an image
            images = convert_from_path(pdf_path, first_page=1, last_page=1)

            # Save the image
            for i, image in enumerate(images):
                # Create the output file path
                base_name = os.path.basename(pdf_path)
                name_without_ext = os.path.splitext(base_name)[0]
                image_path = os.path.join(output_folder, f"{name_without_ext}.jpg")

                # Resize the image
                image.thumbnail(output_size, Image.LANCZOS)

                # Save the image
                image.save(image_path, 'JPEG')

            logger.info(f'Successfully converted {pdf_path} to image and saved at {image_path}')

        except Exception as e:
            logger.error(f'Failed to convert {pdf_path} to image: {e}')


def parallel_convert_pdf_to_image(pdf_folder, output_folder, output_size=(1920, 2560)): # attention
    # Create 'images' directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all PDF files in the folder
    pdf_files = [os.path.join(pdf_folder, filename) for filename in os.listdir(pdf_folder) if filename.lower().endswith('.pdf')]

    # Use a ThreadPoolExecutor to parallelize the conversion process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(convert_pdf_to_image, pdf_files, [output_folder]*len(pdf_files), [output_size]*len(pdf_files))

# Usage
parallel_convert_pdf_to_image('./pdfs_1077', './images_1920_2560') # attention


# 1280, 1600
# 1440, 1920
# 1920, 2560

# 1080, 1440
# 1140, 1520
# 1260, 1680
# 1320, 1760
# 1380, 1840
# 1500, 2000
# 1560, 2080
# 1620, 2160
# 1680, 2240
# 1740, 2320
# 1800, 2400
# 1860, 2480