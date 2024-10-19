import os
import shutil

def empty_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Loop through all the contents of the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Check if it's a file or directory and remove accordingly
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # Remove file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and its contents
        print(f'All contents of {folder_path} have been removed.')
    else:
        print(f'The folder {folder_path} does not exist.')
