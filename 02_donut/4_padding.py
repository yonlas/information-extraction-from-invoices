from PIL import Image
import os

# Replace with your directory path
# image_dir = 'images_1280_1600'
# image_dir = 'images_1440_1920'
# image_dir = 'images_1600_2048'
image_dir = 'images_1920_2560'

# Desired size
# desired_size = (1280, 1600)
# desired_size = (1440, 1920)
# desired_size = (1600, 2048)
desired_size = (1920, 2560)

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # add more conditions if you have other image formats
        img = Image.open(os.path.join(image_dir, filename))
        width, height = img.size

        # If the image is smaller than the desired size, add padding
        if width < desired_size[0] or height < desired_size[1]:
            new_img = Image.new("RGB", desired_size, "white")  # Change "RGB" to "L" for grayscale images
            new_img.paste(img, ((desired_size[0]-width)//2,
                                (desired_size[1]-height)//2))

            # Overwrite the original image with the padded image
            new_img.save(os.path.join(image_dir, filename))

print("Padding process completed.")

# 1280x1600 
# 1440x1920 
# 1600x2048

# 2240 height, 1680 width (0.75 * 2240 = 1680)
# 2080 height, 1560 width (0.75 * 2080 = 1560)
# 2000 height, 1500 width (0.75 * 2000 = 1500)

# Smaller Options:

# 1440 height, 1080 width (0.75 * 1440 = 1080)
# 960 height, 720 width (0.75 * 960 = 720)
# 480 height, 360 width (0.75 * 480 = 360)
# Larger Options:

# 2560 height, 1920 width (0.75 * 2560 = 1920)
# 3200 height, 2400 width (0.75 * 3200 = 2400)
# 3840 height, 2880 width (0.75 * 3840 = 2880)