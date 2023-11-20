import os
import subprocess
import json
import re
from typing import Tuple, Optional


FOLDERS = ["first-stratum"]


FACT_MAP = {
    "1.1.1": "buggy function code",
    "1.1.3": "buggy function docstring",
    "1.3.4": "buggy file name",
}


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


def extract_function_parts(function_code) -> Tuple[Optional[str], Optional[str]]:
    # Regex pattern for matching docstring and function code
    # Handles both types of triple quotes, ignores triple-quoted strings that are not docstrings
    pattern = (
        r'(?s)(def\s+\w+\s*\(\s*.*?\)\s*:\s*)((?:""".*?"""|\'\'\'.*?\'\'\')\s*)?(.*)'
    )

    # Search for matches in the function code
    match = re.search(pattern, function_code)
    if match:
        # Extracting the docstring and function body
        docstring = match.group(2).strip() if match.group(2) else None
        function_body = match.group(1) + match.group(3)

        return (docstring, function_body)
    else:
        return (None, None)


def get_bugid_from_bugdir(bugdir: str):
    parts = bugdir.split("-")
    return "-".join(parts[: len(parts) - 1]) + ":" + parts[len(parts) - 1]


def resolve_buggy_function(buggy_function_info, full_bugdir_path):
    function_code = buggy_function_info["function_code"]
    buggy_function_docstring, buggy_function = extract_function_parts(function_code)

    if buggy_function is not None:
        with open(os.path.join(full_bugdir_path, "f1-1-1.md"), "w") as f:
            f.write(
                f"The {FACT_MAP['1.1.1']} is:\n\n```python\n{buggy_function}\n```\n"
            )
    else:
        print_in_red("FATAL: the buggy function does not exist")

    if buggy_function_docstring is not None:
        with open(os.path.join(full_bugdir_path, "f1-1-3.md"), "w") as f:
            f.write(
                f"The {FACT_MAP['1.1.3']} is:\n\n```python\n{buggy_function_docstring}\n```\n"
            )


def resolve_file_info(filename, file_info, full_bugdir_path):
    with open(os.path.join(full_bugdir_path, "f1-3-4.md"), "w") as f:
        f.write(f"The {FACT_MAP['1.3.4']} is:\n\n```text\n{filename}\n```\n")

    for buggy_function_info in file_info["buggy_functions"]:
        resolve_buggy_function(buggy_function_info, full_bugdir_path)


def resolve_test_data(test_data, full_bugdir_path_):
    pass


def collect_facts(bugid: str, full_bugdir_path: str):
    subprocess.run(["bgp", "clone", "--bugids", bugid])
    console_output = subprocess.run(
        ["bgp", "extract_features", "--bugids", bugid], capture_output=True
    )
    decoded_string = console_output.stdout.decode("utf-8")
    json_output = json.loads(decoded_string)

    # write bug-data.json file
    # with open(os.path.join(full_bugdir_path, "bug-data.json"), "w") as f:
    #     json.dump(json_output, f, indent=4)

    bug_record = json_output[bugid]
    for filename, file_info in bug_record.items():
        if filename == "test_data":
            resolve_test_data(file_info, full_bugdir_path)
        else:
            resolve_file_info(filename, file_info, full_bugdir_path)


collect_facts("black:10", "first-stratum/black-10")
