# from PIL import Image

# def resize_image(input_path, output_path, new_width_cm):
#     # Open the image
#     image = Image.open(input_path)

#     # Calculate the new height in pixels based on the desired width in centimeters
#     dpi = image.info['dpi'][0] if 'dpi' in image.info else 72  # Default DPI if not specified
#     new_width_pixels = int(new_width_cm * dpi / 2.54)
#     aspect_ratio = image.width / image.height
#     new_height_pixels = int(new_width_pixels / aspect_ratio)

#     # Resize the image
#     resized_image = image.resize((new_width_pixels, new_height_pixels), Image.ANTIALIAS)

#     # Save the resized image
#     resized_image.save(output_path, dpi=(dpi, dpi))

# # Example usage
# input_path = '/home/gemmara/Pictures/seri2/c.jpg'
# output_path = '/home/gemmara/Downloads/py_size/c(1).jpg'
# new_width_cm = 30  # Desired width in centimeters

# resize_image(input_path, output_path, new_width_cm)


import os
from PIL import Image

def resize_images_in_folder(input_folder, output_folder, new_width_cm):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path, new_width_cm)

def resize_image(input_path, output_path, new_width_cm):
    image = Image.open(input_path)
    dpi = image.info['dpi'][0] if 'dpi' in image.info else 72
    new_width_pixels = int(new_width_cm * dpi / 2.54)
    aspect_ratio = image.width / image.height
    new_height_pixels = int(new_width_pixels / aspect_ratio)
    resized_image = image.resize((new_width_pixels, new_height_pixels), Image.ANTIALIAS)
    resized_image.save(output_path, dpi=(dpi, dpi))

# Example usage

input_folder = '/home/gemmara/Pictures/seri2/'
output_folder = '/home/gemmara/Downloads/py_size/'
new_width_cm = 30  # Desired width in centimeters

resize_images_in_folder(input_folder, output_folder, new_width_cm)
