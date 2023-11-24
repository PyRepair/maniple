import argparse
import os
import shutil
import subprocess
import json
import re
from typing import List, Tuple, Optional


FLAG_OVERWRITE = False


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


class Facts:
    """
    This class will parse the output from `bgp extract_features` tool and
    process the facts in a way that can be eaily used to construct a prompt
    """

    FACT_MAP = {
        "1.1.1": "buggy function code",
        "1.1.3": "buggy function docstring",
        "1.3.4": "buggy file name",
        "2.1.1": "test function code",
        "2.1.2": "test file name",
        "2.2": "stacktrace and error message",
    }

    def __init__(self, bug_record: dict) -> None:
        self.facts = dict()

    def load_from_json_object(self, bug_record: dict) -> None:
        """
        The command `bgp extract_features ...` returns a JSON object with following schema:

        ```json
        {
            "youtube-dl:28": { "buggy_file_path": { ... } }
        }
        ```

        This method only concerns the fact per bug, the expected format for bug_record would be:

        ```json
        {
            "buggy_file_path1": { ... },
            "buggy_file_path2": { ... }
        }
        ```
        """
        for filename, file_info in bug_record.items():
            if filename == "test_data":
                for test_data in file_info:
                    self._resolve_test_data(test_data)
            else:
                self._resolve_file_info(filename, file_info)

    def _resolve_file_info(self, filename, file_info):
        self.facts["1.3.4"] = filename

        for buggy_function_info in file_info["buggy_functions"]:
            self._resolve_buggy_function(buggy_function_info)

    @staticmethod
    def _extract_function_parts(function_code) -> Tuple[Optional[str], Optional[str]]:
        # Updated regex pattern to capture decorators, leading indentation, function declaration, docstring (if any), and the function body
        pattern = r'(?s)(^\s*)((?:@.*\s*)*)(def\s+\w+\s*\(\s*.*?\)\s*:\s*)((?:""".*?"""|\'\'\'.*?\'\'\')\s*)?(.*)'

        # Search for matches in the function code
        match = re.search(pattern, function_code)
        if match:
            # Extracting the leading indentation, decorators, docstring, and function body
            indentation = match.group(1)
            decorators = match.group(2) if match.group(2) else ""
            docstring = match.group(4).strip() if match.group(4) else None
            function_body = indentation + decorators + match.group(3) + match.group(5)

            return (docstring, function_body)
        else:
            return (None, None)

    def _resolve_buggy_function(self, buggy_function_info):
        function_code = buggy_function_info["function_code"]
        buggy_function_docstring, buggy_function = Facts._extract_function_parts(
            function_code
        )

        if buggy_function is not None:
            self.facts["1.1.1"] = buggy_function
        else:
            print_in_red("FATAL: the buggy function does not exist")

        if buggy_function_docstring is not None:
            self.facts["1.1.3"] = buggy_function_docstring

    @staticmethod
    def _split_error_message(error_message) -> List[dict]:
        lines = error_message.split("\n")
        chunks = []
        current_chunk = []
        current_label = ""

        for line in lines:
            # Determine if the line is an error message or stacktrace
            label = "error_message" if line.startswith("E") else "stacktrace"

            # If we are starting a new chunk, add the previous chunk to the list
            if label != current_label and current_chunk:
                record = {"label": current_label, "content": "\n".join(current_chunk)}
                chunks.append(record)
                current_chunk = []

            # Add the line to the current chunk and update the current label
            current_chunk.append(line)
            current_label = label

        # Add the last chunk to the list
        if current_chunk:
            record = {"label": current_label, "content": "\n".join(current_chunk)}
            chunks.append(record)

        return chunks

    def _resolve_test_data(self, test_data):
        test_file_name = test_data["test_path"]
        self.facts["2.1.2"] = test_file_name

        test_function_code = test_data["test_function_code"]
        self.facts["2.1.1"] = test_function_code

        full_test_error = test_data["full_test_error"]
        error_stacktrace_chunks = Facts._split_error_message(full_test_error)
        self.facts["2.2"] = error_stacktrace_chunks


def collect_facts(bugid: str, dir_path: str):
    full_bugdir_path = os.path.join(dir_path, "-".join(bugid.split(":")))
    if not os.path.exists(full_bugdir_path):
        os.makedirs(full_bugdir_path)

    if FLAG_OVERWRITE:
        if shutil.which("bgp") is None:
            print_in_red(
                """FATAL: bgp command not found. 
                        Try to install it by following the instruction from 
                        https://github.com/PyRepair/PyRepair/tree/master/pyr_benchmark_wrangling"""
            )
            exit(1)

        subprocess.run(["bgp", "clone", "--bugids", bugid], check=True)
        console_output = subprocess.run(
            ["bgp", "extract_features", "--bugids", bugid],
            capture_output=True,
            check=True,
        )

        decoded_string = console_output.stdout.decode("utf-8")
        json_output = json.loads(decoded_string)

        # write bug-data.json file
        with open(os.path.join(full_bugdir_path, "bug-data.json"), "w") as f:
            json.dump(json_output, f, indent=4)

    else:
        with open(os.path.join(full_bugdir_path, "bug-data.json"), "r") as f:
            json_output = json.load(f)

    bug_record = json_output[bugid]
    facts = Facts(bug_record)
    facts.load_from_json_object(bug_record)

    write_markdown_files(facts, full_bugdir_path)


def write_markdown_files(facts: Facts, output_dir: str):
    # write facts.json file
    with open(os.path.join(output_dir, "facts.json"), "w") as f:
        json.dump(facts.facts, f, indent=4)

    for fact_key, fact_content in facts.facts.items():
        if fact_key == "2.2":
            error_message_chunks = "\n".join(
                [
                    content["content"]
                    for content in fact_content
                    if content["label"] == "error_message"
                ]
            )
            with open(os.path.join(output_dir, "f2-2-1.md"), "w") as f:
                name = "error message"
                f.write(f"# {name}\n\n```text\n{error_message_chunks}\n```")

            stacktrace_chunks = "\n".join(
                [
                    content["content"]
                    for content in fact_content
                    if content["label"] == "stacktrace"
                ]
            )
            with open(os.path.join(output_dir, "f2-2-2.md"), "w") as f:
                name = "stacktrace"
                f.write(f"# {name}\n\n```text\n{stacktrace_chunks}\n```")
        else:
            filename = "f" + fact_key.replace(".", "-") + ".md"
            with open(os.path.join(output_dir, filename), "w") as f:
                fact_name = Facts.FACT_MAP[fact_key]
                if "code" in fact_name:
                    fact_content = "```python\n" + fact_content + "\n```"
                else:
                    fact_content = "```text\n" + fact_content + "\n```"
                f.write(f"""# {Facts.FACT_MAP[fact_key]}\n\n{fact_content}""")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--bugids",
        type=lambda s: s.split(","),
        help="specify a list of bugids to collect facts, like `pandas:30,scikit-learn:1`",
    )
    args_parser.add_argument("-o", "--output-dir", help="specify the output directory")
    args_parser.add_argument("--overwrite", action="store_true")
    args = args_parser.parse_args()

    if args.overwrite:
        FLAG_OVERWRITE = True

    if args.output_dir is None:
        args_parser.print_help()
        exit(1)

    bugids = args.bugids
    if bugids is None:
        bugids = []
        dirs = os.listdir(args.output_dir)
        for directory in dirs:
            if not os.path.isdir(os.path.join(args.output_dir, directory)):
                continue
            parts = directory.split("-")
            bugids.append(f"{'-'.join(parts[:-1])}:{parts[-1]}")

    for bugid in bugids:
        collect_facts(bugid, args.output_dir)
