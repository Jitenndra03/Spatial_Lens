import os

def rename_images(directory_path, prefix = "chessboard_", image_extension = ('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG')):

    try:
        image_files = [file for file in os.listdir(directory_path)
                       if file.lower().endswith(image_extension)]

        image_files.sort()

        for index, old_name in enumerate(image_files, start=1):

            file_extension = os.path.splitext(old_name)[1]

            new_name = f"{prefix}{index}{file_extension}"

            old_file_path = os.path.join(directory_path, old_name)
            new_file_path = os.path.join(directory_path, new_name)

            os.rename(old_file_path, new_file_path)

            print(f"Renamed {old_name} to {new_name}")

        print("All files renamed successfully.")

    except Exception as e:
        print(f"Error occurred while renaming files: {str(e)}")


directory_path = "/home/jitendra/Documents/Spatial_Lens/chessboard_images"
rename_images(directory_path)



