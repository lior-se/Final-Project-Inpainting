import cv2
import structural_similarity_modified as sst  # Import the modified structural_similarity function
#import structural_sim2 as sst
from skimage.metrics import structural_similarity as ssim_skimage

def main():
    # Load images
    img1 = cv2.imread('original/C0017.bmp')
    img2 = cv2.imread('Wavelet/C0017_comp_wavlet.png')

    if img1 is None or img2 is None:
        print("Error loading images.")
        return


    # Set parameters
    alpha = 0.8152
    beta = 41.17
    gamma = 0.1776

    # Compute SSIM
    ssim_value = sst.structural_similarity(img1, img2, alpha=alpha, beta=beta, gamma=gamma,
                                                                      multichannel=True)

    print(f'SSIM (alpha={alpha}, beta={beta}, gamma={gamma}): {ssim_value}')

    ssim_builtin, _ = ssim_skimage(img1, img2, full=True, multichannel=True)
    print(f'SSIM (skimage): {ssim_builtin}')

if __name__ == "__main__":
    main()