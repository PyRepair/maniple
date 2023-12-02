import os


def clear_files(path: str):
    # Traverse all directories and files
    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the filename starts with 'f'
            if file.startswith("f") and not file.startswith("f3"):
                # Delete the file
                os.remove(os.path.join(root, file))
