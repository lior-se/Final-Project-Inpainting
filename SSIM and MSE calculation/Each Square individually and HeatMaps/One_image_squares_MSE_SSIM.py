import cv2
import numpy as np
from skimage.metrics import mean_squared_error, structural_similarity as ssim
import matplotlib.pyplot as plt
import pandas as pd

# Load images and mask
original = cv2.imread('examples/original/C0101.bmp')
damaged = cv2.imread('examples/cropped_wavelet/C0101_comp_wavlet.png')
mask = cv2.imread('general_mask.png', cv2.IMREAD_GRAYSCALE)

# Invert mask if necessary (ensure white squares where calculations are needed)
mask = cv2.bitwise_not(mask)

# Identify squares using the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mse_values = []
ssim_values = []
positions = []  # To store the rectangle dimensions and positions

# Calculate MSE and SSIM for each contour (square)
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    original_square = original[y:y+h, x:x+w]
    damaged_square = damaged[y:y+h, x:x+w]

    # Calculate MSE and SSIM for each color channel and average them
    current_mse = mean_squared_error(original_square, damaged_square)
    current_ssim = ssim(original_square, damaged_square, multichannel=True)

    mse_values.append(current_mse)
    ssim_values.append(current_ssim)
    positions.append((x, y, w, h))  # Store the dimensions and position

# Create histograms
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(mse_values, bins=20, color='blue')
plt.title('Histogram of MSE')
plt.subplot(1, 2, 2)
plt.hist(ssim_values, bins=20, color='green')
plt.title('Histogram of SSIM')
plt.savefig('histograms.png')

# Save results to Excel
df = pd.DataFrame({
    'X': [pos[0] for pos in positions],
    'Y': [pos[1] for pos in positions],
    'Width': [pos[2] for pos in positions],
    'Height': [pos[3] for pos in positions],
    'MSE': mse_values,
    'SSIM': ssim_values
})
df.to_excel('resultsC0101.xlsx', index=False)
