from PIL import Image
import os

def crop_image(input_path, output_path):
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the coordinates to crop the image to 512x512 centered
        width, height = img.size  # should be 529x529 as per your original image
        left = (width - 512) // 2
        top = (height - 512) // 2
        right = (width + 512) // 2
        bottom = (height + 512) // 2

        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))

        # Save the cropped image
        cropped_img.save(output_path)

'''
crop_image("general_mask.png","general_mask.png")
for i in range(2724, 2753):
    crop_image(f"second_test/pgbz/image{str(i).zfill(4)}_comp_pgbz.png",
               f"second_test/pgbz_cropped/C{str(i).zfill(4)}_comp_pgbz.png")
    #crop_image(f"examples/our_test_input/C{str(i).zfill(4)}_comp_pgbz.png",f"examples/input_cropped/C{str(i).zfill(4)}_comp_pgbz.png")
    #crop_image(f"examples/our_test_output/C{str(i).zfill(4)}_comp_pgbz_output.png",
    #           f"examples/output_cropped/C{str(i).zfill(4)}_comp_pgbz_output.png")
    #crop_image(f"examples/our_test_output_celebhq/NB{str(i).zfill(4)}_comp_pgbz_output.png",
    #           f"examples/cropped_output_celebhq/NB{str(i).zfill(4)}_comp_pgbz_output.png")
    #crop_image(f"examples/our_test_output_celebhq/C{str(i).zfill(4)}_comp_pgbz_output.png",
    #           f"examples/cropped_output_celebhq/C{str(i).zfill(4)}_comp_pgbz_output.png")
    #crop_image(f"examples/our_test_input/C{str(i).zfill(4)}_comp_pgbz.png",
               #f"examples/cropped_pbgz/C{str(i).zfill(4)}_comp_pgbz.png")

    #crop_image("examples/places2/C0010_comp_pgbz_output1.png","examples/places2/C0010_comp_pgbz_output1_crop.png")
    #crop_image("examples/places2/C0010_comp_pgbz_output2.png","examples/places2/C0010_comp_pgbz_output2_crop.png")
'''
image_directory = '750images_tests/Val_Comp/To_Be_compressed_compressed_wavelet'

# Iterate over all files in the directory
for filename in os.listdir(image_directory):
    # Create the full path to the file
    file_path = os.path.join(image_directory, filename)

    # Ensure it's a file and not a directory
    if os.path.isfile(file_path):
        # Crop the image and save it back to the same path
        crop_image(file_path, file_path)

print("All images have been cropped and saved in the same directory.")