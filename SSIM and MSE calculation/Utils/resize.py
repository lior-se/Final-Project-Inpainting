import os
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage.util import img_as_ubyte


def resize_images_in_folder(input_folder, output_folder, target_size=(256, 256)):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all image filenames in the input folder
    filenames = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for filename in filenames:
        # Load the image
        img = imread(os.path.join(input_folder, filename))

        # Resize the image to the target size
        img_resized = resize(img, target_size, anti_aliasing=True)

        # Convert the image back to unsigned 8-bit integer format for saving
        img_resized = img_as_ubyte(img_resized)

        # Save the resized image to the output folder
        imsave(os.path.join(output_folder, filename), img_resized)
        print(f"Resized and saved {filename} to {output_folder}")


# Define your input and output directories
input_folder = 'images'
output_folder = 'images'

# Resize all images in the input folder
resize_images_in_folder(input_folder, output_folder)
