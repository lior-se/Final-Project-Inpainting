from PIL import Image
import os

# Paths to directories and mask file
source_dir = 'examples/original/'
mask_path = 'examples/places2/mask_to_reuze_cropped.png'
target_dir = 'examples/original_mask/'

# Create the target directory if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Load the mask image
mask = Image.open(mask_path)

# Process each image in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".png"):  # check for PNG images
        img_path = os.path.join(source_dir, filename)
        img = Image.open(img_path)

        # Ensure the image and mask sizes match
        if img.size != mask.size:
            # Resize mask to match image size
            mask_resized = mask.resize(img.size, Image.ANTIALIAS)
        else:
            mask_resized = mask

        # Place the mask over the image
        img.paste(mask_resized, (0, 0), mask_resized)

        # Save the masked image
        img.save(os.path.join(target_dir, filename))
        print(f"Processed {filename}")

print("All images processed.")
