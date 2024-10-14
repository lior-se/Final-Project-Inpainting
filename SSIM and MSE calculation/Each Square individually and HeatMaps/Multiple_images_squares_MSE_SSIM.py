import cv2
import numpy as np
from skimage.metrics import mean_squared_error, structural_similarity as ssim
import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join

def load_images_from_folder(folder):
    """Load images and their filenames from a specified folder."""
    filenames = [f for f in listdir(folder) if isfile(join(folder, f))]
    filenames.sort()
    images = [cv2.imread(join(folder, filename)) for filename in filenames]
    return images, filenames

def process_images(original, damaged, mask):
    """Calculate MSE and SSIM for areas defined by a mask between two images."""
    inverted_mask = cv2.bitwise_not(mask)
    contours, _ = cv2.findContours(inverted_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mse_values, ssim_values, positions = [], [], []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        original_square = original[y:y+h, x:x+w]
        damaged_square = damaged[y:y+h, x:x+w]
        mse_values.append(mean_squared_error(original_square, damaged_square))
        ssim_values.append(ssim(original_square, damaged_square, multichannel=True))
        positions.append((x, y, w, h))
    return mse_values, ssim_values, positions

def save_histograms(mse_values, ssim_values, prefix):
    """Save histograms of MSE and SSIM values."""
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(mse_values, bins=20, color='blue')
    plt.title(f'{prefix} MSE Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.subplot(1, 2, 2)
    plt.hist(ssim_values, bins=20, color='green')
    plt.title(f'{prefix} SSIM Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.savefig(f'{prefix}_histograms.png')
    plt.close()

mask = cv2.imread('general_mask.png', cv2.IMREAD_GRAYSCALE)
original_images, original_filenames = load_images_from_folder('squares/original/')
pb_gz_images, _ = load_images_from_folder('squares/PBGZ/')
wavelet_images, _ = load_images_from_folder('squares/Wavelet/')
places2_images, _ = load_images_from_folder('squares/Places2/')

writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')

for index, (original, orig_filename) in enumerate(zip(original_images, original_filenames)):
    pbgz = pb_gz_images[index]
    wavelet = wavelet_images[index]
    places2 = places2_images[index]

    # Process and append results for the first type of damaged image
    mse_values, ssim_values, positions = process_images(original, pbgz, mask)
    result_df = pd.DataFrame({
        'X': [pos[0] for pos in positions],
        'Y': [pos[1] for pos in positions],
        'Width': [pos[2] for pos in positions],
        'Height': [pos[3] for pos in positions],
        'MSE_PBGZ': mse_values,
        'SSIM_PBGZ': ssim_values
    })
    prefix_pbgz = f"{orig_filename.split('.')[0]}_PBGZ"
    save_histograms(mse_values, ssim_values, prefix_pbgz)
    # Process and append results for the remaining types of damaged images
    for key, damaged in zip(['Places2','Wavelet'], [places2, wavelet]):
        mse_values, ssim_values, _ = process_images(original, damaged, mask)
        result_df[f'MSE_{key}'] = mse_values
        result_df[f'SSIM_{key}'] = ssim_values
        prefix = f"{orig_filename.split('.')[0]}_{key}"
        save_histograms(mse_values, ssim_values, prefix)

    # Write to specific sheet in the Excel file using the original image filename (without extension)
    result_df.to_excel(writer, sheet_name=orig_filename.split('.')[0], index=False)

writer.save()

