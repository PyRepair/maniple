import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

from maniple.utils.misc import iter_bugid_folders

def is_incomplete_code(code: str):
    # match case: "# omitted code..."
    pattern = r".*#.*omitted.*\.\.\..*"
    # keyword case
    sensitive_words = [
        "rest of the",
        "previous code unchanged",
        "remain unchanged"
    ]
    for line in code.split("\n"):
        match = re.search(pattern, line)
        if match:
            return True
        for word in sensitive_words:
            if word.lower() in line.lower():
                return True
    return False


def detect_incomplete_code(output_dir):
    bugid_counter = defaultdict(list)
    for bugid, project_folder, bugid_folder in iter_bugid_folders(Path(output_dir)):
        for bitvector_folder in bugid_folder.iterdir():
            if not bitvector_folder.is_dir():
                continue
            for response_file in bitvector_folder.glob("*response*.json"):
                with open(response_file, "r") as f:
                    response_data = json.load(f)
                    bugid_data = response_data[project_folder.name][0]
                    fix_patch = bugid_data["replace_code"]
                    if not fix_patch:
                        continue
                if is_incomplete_code(fix_patch):
                    bugid_counter[bugid].append(str(response_file.with_suffix(".md")))

    with open("result.json", "w") as f:
        json.dump(bugid_counter, f, indent=4)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("output_dir", help="the name of the dataset to initialize")
    args = arg_parser.parse_args()

    detect_incomplete_code(args.output_dir)
