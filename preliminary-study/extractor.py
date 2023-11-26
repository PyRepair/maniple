import argparse
import os
import shutil
import subprocess
import json
import re
from typing import List


FLAG_OVERWRITE = False


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


class NotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Facts:
    """
    This class will parse the output from `bgp extract_features` tool and
    process the facts in a way that can be eaily used to construct a prompt
    """

    FACT_MAP = {
        "1.1.1": "buggy function code",
        "1.1.2": "buggy function docstring",
        "1.1.3": "invoked function signature",
        "1.2.1": "buggy class signature",
        "1.2.2": "buggy class docstring",
        "1.2.3": "relevant buggy class method signature",
        "1.2.4": "invoked method signature",
        "1.3.1": "relavent function signature",
        "1.3.2": "buggy file name",
        "1.3.3": "relevant variables",
        "1.3.4": "invoked function signature",
        "1.4.1": "runtime variable type",
        "1.4.2": "runtime variable value",
        "2.1.1": "test function code",
        "2.1.2": "test file name",
        "2.2.1": "error message",
        "2.2.2": "stacktrace",
        "3.1.1": "issue title",
        "3.1.2": "issue description",
    }

    def __init__(self, bug_record: dict) -> None:
        self.facts = dict()
        self._variables_in_methods = []

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
        if len(bug_record) > 2:
            raise NotSupportedError(
                "multiple buggy files are not supported at the moment"
            )

        for filename, file_info in bug_record.items():
            if filename == "test_data":
                for test_data in file_info:
                    self._resolve_test_data(test_data)
            else:
                self._resolve_file_info(filename, file_info)

    def _resolve_file_info(self, filename, file_info):
        self.facts["1.3.2"] = filename

        if len(file_info["buggy_functions"]) > 1:
            raise NotSupportedError(
                "multiple buggy functions are not supported at the moment"
            )
        for buggy_function_info in file_info["buggy_functions"]:
            self._resolve_buggy_function(buggy_function_info)

        called_in_scope_functions = []
        for fn in file_info["inscope_functions"]:
            if self._is_this_func_called(fn):
                called_in_scope_functions.append(fn)
        if len(called_in_scope_functions) > 0:
            self.facts["1.3.4"] = called_in_scope_functions

    def _is_this_func_called(self, sig):
        for v in self._variables_in_methods:
            var = v.split(".")[-1]
            if Facts._extract_function_name(sig) == var:
                return True
        return False

    @staticmethod
    def _extract_function_name(signature):
        """
        Extracts and returns the function name from a given function signature string.

        Args:
        signature (str): A string representing the function signature.

        Returns:
        str: The name of the function.
        """
        # Split the signature string at the first opening parenthesis
        parts = signature.split("(")
        # The first part is the function name
        # Stripping to remove any leading or trailing spaces
        return parts[0].strip()

    def _resolve_buggy_function(self, buggy_function_info):
        buggy_function = buggy_function_info["function_code"]
        buggy_function_docstring = buggy_function_info["docstring"]

        if buggy_function is not None:
            self.facts["1.1.1"] = Facts.remove_docstring_from_source(buggy_function)
        else:
            print_in_red("FATAL: the buggy function does not exist")

        if buggy_function_docstring is not None:
            self.facts["1.1.2"] = buggy_function_docstring

        self._variables_in_methods = buggy_function_info["filtered_variables"]

        if buggy_function_info["class_data"] is not None:
            self._resolve_class_info(buggy_function_info["class_data"])

    def _resolve_class_info(self, buggy_class_info):
        class_signature = buggy_class_info["signature"]
        class_decorators = buggy_class_info["class_decorators"]

        if class_decorators is not None and len(class_decorators) > 0:
            for decorator in class_decorators[::-1]:
                class_signature = "@" + decorator + "\n" + class_signature

        self.facts["1.2.1"] = class_signature

        class_docstring = buggy_class_info["docstring"]
        if class_docstring is not None:
            self.facts["1.2.2"] = class_docstring

        used_methods = []
        for method in buggy_class_info["functions"]:
            if self._is_this_func_called(method):
                used_methods.append(method)
        if len(used_methods) > 0:
            self.facts["1.2.4"] = used_methods

    @staticmethod
    def remove_docstring_from_source(function_source):
        # Regex to match docstrings: Triple quotes (either """ or ''')
        # followed by any characters (non-greedy) and then triple quotes again
        # The re.DOTALL flag allows the dot (.) to match newlines as well
        pattern = r"\"\"\".*?\"\"\"|\'\'\'.*?\'\'\'"
        return re.sub(pattern, "", function_source, flags=re.DOTALL)

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
        test_function_code = test_data["test_function_code"]
        if self.facts.get("2.1.1") is None:
            self.facts["2.1.1"] = [test_function_code]
        else:
            self.facts["2.1.1"].append(test_function_code)

        test_file_name = test_data["test_path"]
        if self.facts.get("2.1.2") is None:
            self.facts["2.1.2"] = [test_file_name]
        else:
            self.facts["2.1.2"].append(test_file_name)

        if self.facts.get("2.2.1") is None:
            self.facts["2.2.1"] = []
        if self.facts.get("2.2.2") is None:
            self.facts["2.2.2"] = []

        full_test_error = test_data["full_test_error"]
        error_stacktrace_chunks = Facts._split_error_message(full_test_error)

        full_stacktrace = []
        full_error_message = []

        is_error_message = None
        for chunk in error_stacktrace_chunks:
            if chunk["label"] == "stacktrace":
                if is_error_message is not None and not is_error_message:
                    raise NotSupportedError("2 error message follow together")
                is_error_message = False
                full_stacktrace.append(chunk["content"])
            elif chunk["label"] == "error_message":
                if is_error_message is not None and is_error_message:
                    raise NotSupportedError("2 stack traces follow together")
                is_error_message = True
                full_error_message.append(chunk["content"])

        if self.facts.get("2.2.1") is None:
            self.facts["2.2.1"] = []
        else:
            self.facts["2.2.1"].append(full_error_message)

        if self.facts.get("2.2.2") is None:
            self.facts["2.2.2"] = []
        else:
            self.facts["2.2.2"].append(full_stacktrace)


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

    def extract_code_blocks(md_content):
        # Regular expression pattern to match code blocks
        # The pattern looks for triple backticks, optionally followed by an identifier (like python, js, etc.)
        # and then any content until the closing triple backticks, across multiple lines
        pattern = r"```[a-zA-Z]*\n(.*?)```"

        # Find all matches in the Markdown content
        matches = re.findall(pattern, md_content, flags=re.DOTALL)

        return matches

    write_markdown_files(facts, full_bugdir_path)

    if os.path.exists(os.path.join(full_bugdir_path, "f3-1-1.md")):
        with open(os.path.join(full_bugdir_path, "f3-1-1.md"), "r") as f:
            facts.facts["3.1.1"] = extract_code_blocks(f.read())

    if os.path.exists(os.path.join(full_bugdir_path, "f3-1-2.md")):
        with open(os.path.join(full_bugdir_path, "f3-1-2.md"), "r") as f:
            facts.facts["3.1.2"] = extract_code_blocks(f.read())

    # write facts.json file
    with open(os.path.join(full_bugdir_path, "facts.json"), "w") as f:
        json.dump(facts.facts, f, indent=4)

    print(f"bugid: {bugid}")
    if facts.facts.get("1.2.4") is None:
        print(f"method ref num: 0")
    else:
        print(f"method ref num: {len(facts.facts['1.2.4'])}")

    if facts.facts.get("1.3.4") is None:
        print(f"in_scope_functions ref num: 0")
    else:
        print(f"in_scope_functions ref num: {len(facts.facts['1.3.4'])}")


def write_markdown_files(facts: Facts, output_dir: str):
    for fact_key, fact_content in facts.facts.items():
        if isinstance(fact_content, list):

            def flatten_and_join(arr):
                # Function to recursively flatten the array
                def flatten(array):
                    for element in array:
                        if isinstance(element, list):
                            # If the element is a list, extend the result with the flattened list
                            yield from flatten(element)
                        else:
                            # Otherwise, just yield the element
                            yield element

                # Flatten the array and join with newlines
                return "\n".join(map(str, flatten(arr)))

            fact_content = flatten_and_join(fact_content)

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
        try:
            collect_facts(bugid, args.output_dir)
        except NotSupportedError as e:
            print_in_red(f"ERROR: {e}")
            print_in_red(f"Skip {bugid}")
