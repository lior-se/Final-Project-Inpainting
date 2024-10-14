import numpy as np
import pandas as pd
from skimage.metrics import mean_squared_error, structural_similarity
from skimage.io import imread
from os import listdir
from os.path import isfile, join

def load_images_from_folder(folder):
    images = []
    filenames = [f for f in listdir(folder) if isfile(join(folder, f))]
    filenames.sort()  # Ensure the order is consistent
    for filename in filenames:
        img = imread(join(folder, filename))
        if img is not None:
            images.append(img)
    return images, filenames

def masked_metrics(original, altered, mask):
    assert original.shape[:2] == altered.shape[:2] == mask.shape, "All images must have the same spatial dimensions"
    # Create a boolean mask where black pixels (0) are True and others are False
    bool_mask = mask == 0
    # Apply the mask to each channel of the images
    original_masked = original * np.stack([bool_mask]*3, axis=-1)  # Stack the mask across the color channels
    altered_masked = altered * np.stack([bool_mask]*3, axis=-1)
    # Calculate MSE and SSIM on non-zero elements (masked areas)
    non_zero_mask = original_masked.sum(axis=2) != 0  # Find where not all channels are zero (unmasked areas)
    mse = mean_squared_error(original_masked[non_zero_mask], altered_masked[non_zero_mask])
    ssim = structural_similarity(original_masked[non_zero_mask], altered_masked[non_zero_mask], multichannel=True, data_range=original.max() - original.min())
    return mse, ssim

# Load the general mask
mask_path = 'general_mask.png'
mask = imread(mask_path, as_gray=True)  # Ensure the mask is in grayscale

# Directories containing the original and altered images
original_images_dir = 'examples/original/'
altered_images_dir = 'examples/cropped_wavelet/'

# Load images
original_images, original_filenames = load_images_from_folder(original_images_dir)
altered_images, altered_filenames = load_images_from_folder(altered_images_dir)

assert len(original_images) == len(altered_images), "Image count mismatch between folders"

results_df = pd.DataFrame(columns=['Filename', 'MSE', 'SSIM'])

for orig_img, alt_img, filename in zip(original_images, altered_images, original_filenames):
    mse, ssim = masked_metrics(orig_img, alt_img, mask)
    results_df = results_df.append({'Filename': filename, 'MSE': mse, 'SSIM': ssim}, ignore_index=True)

results_df.to_excel('wavelet_mask_results.xlsx', index=False)
