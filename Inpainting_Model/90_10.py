import os
import shutil
import random

# Path to the directory containing the images
source_dir = "C:\\Users\\Mendel\\Desktop\\tosend\\whole_dataset"

# Paths for the train and validation directories
train_dir = 'training_data/training'
validation_dir = 'training_data/validation'

# Create train and validation directories
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# Get a list of images from the source directory
images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

# Shuffle the list of images
random.shuffle(images)

# Calculate the split index for 90% train, 10% validation
split_index = int(0.9 * len(images))

# Split the images into train and validation sets
train_images = images[:split_index]
validation_images = images[split_index:]

# Move the images to the respective directories
for image in train_images:
    shutil.move(os.path.join(source_dir, image), os.path.join(train_dir, image))

for image in validation_images:
    shutil.move(os.path.join(source_dir, image), os.path.join(validation_dir, image))

print(f'Moved {len(train_images)} images to {train_dir} and {len(validation_images)} images to {validation_dir}.')
