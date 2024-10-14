import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

# Load the data from the Excel file
file_path = 'Results_each_square.xlsx'
sheet_name = 'NB0103'
data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

# Calculate the difference in SSIM values between PBGZ and Wavelet for each square
data['MSE_Diff'] = data['MSE_PBGZ'] - data['MSE_Wavelet']

# Initialize the image
image_size = (512, 512)
image = np.ones((image_size[0], image_size[1], 3))  # Start with a white image

# Define colors
blue = np.array([0, 0, 1])
red = np.array([1, 0, 0])
white = np.array([1, 1, 1])

# Normalize the SSIM difference for coloring
max_diff = data['MSE_Diff'].max()
min_diff = data['MSE_Diff'].min()

# Function to get color based on SSIM difference
def get_color(diff):
    normalized = (diff - min_diff) / (max_diff - min_diff)
    if diff > 0:
        return white * (1 - normalized) + red * normalized
    else:
        return white * (1 - normalized) + blue * normalized

# Color the squares based on the SSIM difference
for index, row in data.iterrows():
    x, y, width, height, mse_diff = int(row['X']), int(row['Y']), int(row['Width']), int(row['Height']), row['MSE_Diff']
    color = get_color(mse_diff)
    image[y:y+height, x:x+width, :] = color

# Plot the image
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('off')
plt.savefig('NB0103_hot_map_MSE.png', dpi=300, bbox_inches='tight')
plt.show()
