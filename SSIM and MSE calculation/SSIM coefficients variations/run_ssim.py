# compute_ssim.py
import os
import cv2
import numpy as np
import pandas as pd
import structural_similarity_modified as sst  # Import the modified structural_similarity function
from skimage.metrics import structural_similarity as ssim_skimage
from tqdm import tqdm


def compute_ssim_for_images(img1, img2, alphas, betas, gammas):
    results = []
    for alpha in alphas:
        for beta in betas:
            for gamma in gammas:
                ssim_value = sst.structural_similarity(img1, img2, alpha=alpha, beta=beta, gamma=gamma,
                                                       multichannel=True)
                results.append((alpha, beta, gamma, ssim_value))
    return results


def main():
    original_dir = 'original'
    pbgz_dir = 'places2'
    wavelet_dir = 'Wavelet'

    # Parameters
    alphas = [0.2, 0.8, 1.3, 2]
    betas = [0.2, 0.8, 1.3, 2]
    gammas = [0.2, 0.8, 1.3, 2]

    columns = ['Image', 'Alpha', 'Beta', 'Gamma', 'SSIM_PBGZ', 'SSIM_Wavelet']
    df = pd.DataFrame(columns=columns)

    original_images = sorted(os.listdir(original_dir))
    pbgz_images = sorted(os.listdir(pbgz_dir))
    wavelet_images = sorted(os.listdir(wavelet_dir))

    for img_name, pbgz_img_name, wavelet_img_name in tqdm(zip(original_images, pbgz_images, wavelet_images),
                                                          total=len(original_images), desc="Processing images"):
        img1_path = os.path.join(original_dir, img_name)
        img1 = cv2.imread(img1_path)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

        # Process PBGZ images
        img2_path = os.path.join(pbgz_dir, pbgz_img_name)
        img2 = cv2.imread(img2_path)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        results_pbgz = compute_ssim_for_images(img1, img2, alphas, betas, gammas)

        # Process Wavelet images
        img3_path = os.path.join(wavelet_dir, wavelet_img_name)
        img3 = cv2.imread(img3_path)
        img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
        results_wavelet = compute_ssim_for_images(img1, img3, alphas, betas, gammas)

        # Combine results for the same image
        for (alpha, beta, gamma, ssim_pbgz), (_, _, _, ssim_wavelet) in zip(results_pbgz, results_wavelet):
            df = df.append({
                'Image': img_name,
                'Alpha': alpha,
                'Beta': beta,
                'Gamma': gamma,
                'SSIM_PBGZ': ssim_pbgz,
                'SSIM_Wavelet': ssim_wavelet
            }, ignore_index=True)

    # Save results to an Excel file
    df.to_excel('ssim_results_places2.xlsx', index=False)
    print("Results saved to ssim_results_places2.xlsx")


if __name__ == "__main__":
    main()
