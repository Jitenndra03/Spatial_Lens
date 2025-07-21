import os
from PIL import Image, ImageEnhance
import random


def augment_images(input_directory, output_directory, augmentations_per_image=5):
    """
    Augments images in the input directory and saves the augmented images in the output directory.

    :param input_directory: Directory containing the original images.
    :param output_directory: Directory where augmented images will be saved.
    :param augmentations_per_image: Number of augmented images to create for each original image.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Supported image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [file for file in os.listdir(input_directory) if file.lower().endswith(image_extensions)]

    transform_count = 0

    for image_file in image_files:
        # Open the image
        img_path = os.path.join(input_directory, image_file)
        image = Image.open(img_path)

        # Generate augmentations
        for i in range(augmentations_per_image):
            augmented_image = image.copy()

            # Apply random transformations
            if random.choice([True, False]):
                angle = random.randint(0, 360)
                augmented_image = augmented_image.rotate(angle, expand=True)

            if random.choice([True, False]):
                flip_type = random.choice(['H', 'V'])  # Horizontal or Vertical flip
                if flip_type == 'H':
                    augmented_image = augmented_image.transpose(Image.FLIP_LEFT_RIGHT)
                elif flip_type == 'V':
                    augmented_image = augmented_image.transpose(Image.FLIP_TOP_BOTTOM)

            if random.choice([True, False]):
                enhancer = ImageEnhance.Brightness(augmented_image)
                brightness_factor = random.uniform(0.5, 1.5)  # Random brightness adjustment
                augmented_image = enhancer.enhance(brightness_factor)

            if random.choice([True, False]):
                enhancer = ImageEnhance.Color(augmented_image)
                color_factor = random.uniform(0.5, 1.5)  # Random color enhancement
                augmented_image = enhancer.enhance(color_factor)

            if random.choice([True, False]):
                width, height = augmented_image.size
                crop_size = random.uniform(0.8, 1.0)  # Random crop between 80%-100%
                x_crop = int(width * crop_size)
                y_crop = int(height * crop_size)
                x_offset = random.randint(0, width - x_crop)
                y_offset = random.randint(0, height - y_crop)
                augmented_image = augmented_image.crop((x_offset, y_offset, x_offset + x_crop, y_offset + y_crop))
                augmented_image = augmented_image.resize((width, height), Image.Resampling.LANCZOS)

            # Save the augmented image
            output_name = f"{os.path.splitext(image_file)[0]}_aug_{i + 1}.jpg"
            output_path = os.path.join(output_directory, output_name)
            augmented_image.save(output_path)
            transform_count += 1

    print(f"Augmented {transform_count} images and saved to {output_directory}")


# Example usage:
input_dir = "/home/jitendra/Documents/Spatial_Lens/chessboard_images"
output_dir = "/home/jitendra/Documents/Spatial_Lens/Augmentated_images"
augment_images(input_dir, output_dir)