from PIL import Image
import pandas as pd
import numpy as np
import openpyxl



def load_image(image_path):
    return Image.open(image_path)


def extract_masked_pixels(base_image, damaged_image, mask_image):
    base_pixels = np.array(base_image)
    damaged_pixels = np.array(damaged_image)
    mask_pixels = np.array(mask_image)

    rows, cols = np.where(mask_pixels[:, :, 0] == 255)

    data = []
    for r, c in zip(rows, cols):
        base_color = base_pixels[r, c]
        damaged_color = damaged_pixels[r, c]

        diff_r = abs(int(damaged_color[0]) - int(base_color[0]))
        diff_g = abs(int(damaged_color[1]) - int(base_color[1]))
        diff_b = abs(int(damaged_color[2]) - int(base_color[2]))

        data.append({
            'Row': r,
            'Column': c,
            'Base R': base_color[0],
            'Base G': base_color[1],
            'Base B': base_color[2],
            'Damaged R': damaged_color[0],
            'Damaged G': damaged_color[1],
            'Damaged B': damaged_color[2],
            'Difference R': diff_r,
            'Difference G': diff_g,
            'Difference B': diff_b
        })

    return data


def write_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)


base_image_path = 'C0013.bmp'
damaged_image_path = 'C0013_comp_pgbz.png'
mask_image_path = 'mask_barre.png'
output_excel_path = 'C0013_pixels_comparison.xlsx'

base_image = load_image(base_image_path)
damaged_image = load_image(damaged_image_path)
mask_image = load_image(mask_image_path)


data = extract_masked_pixels(base_image, damaged_image, mask_image)

write_to_excel(data, output_excel_path)
