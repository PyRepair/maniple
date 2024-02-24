import argparse
from check_utils import bugid_patches
from pathlib import Path


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--bugids", nargs="+", help="The bug ids to check")
    argument_parser.add_argument("--bugid-folder", help="The folder containing the bug id folders")
    args = argument_parser.parse_args()

    bugids = args.bugids
    bugid_folder = Path(args.bugid_folder)

    for bugid in bugids:
        print(bugid_patches(bugid, bugid_folder))
