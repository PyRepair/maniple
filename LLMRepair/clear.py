import argparse
import os


def clear_files(path: str):
    # Traverse all directories and files
    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the filename starts with 'f'
            if file.startswith("f") and not file.startswith("f3"):
                # Delete the file
                os.remove(os.path.join(root, file))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-p", "--path", type=str, required=True, help="Path to the directory"
    )
    args = argparser.parse_args()
    clear_files(args.path)
