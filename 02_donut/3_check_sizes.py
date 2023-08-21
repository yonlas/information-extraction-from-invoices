from PIL import Image
import os
import numpy as np

# Replace with your directory path
# image_dir = 'images_1280_1600'
# image_dir = 'images_1440_1920'
# image_dir = 'images_1600_2048'
image_dir = 'images_1920_2560'

widths = []
heights = []

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # add more conditions if you have other image formats
        img = Image.open(os.path.join(image_dir, filename))
        width, height = img.size
        # Uncomment the following line to print the size of each image
        # print(f'Image {filename} size: {width}x{height}')
        widths.append(width)
        heights.append(height)

# Convert lists to numpy arrays for easy calculation
widths = np.array(widths)
heights = np.array(heights)

print(f'Maximum width: {np.max(widths)}')
print(f'Maximum height: {np.max(heights)}')
print(f'Minimum width: {np.min(widths)}')
print(f'Minimum height: {np.min(heights)}')
print(f'Average width: {np.mean(widths)}')
print(f'Average height: {np.mean(heights)}')

# 1280x1600 
# 1440x1920 
# 1600x2048