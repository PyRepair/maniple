import os
import shutil
import subprocess
import json
import re
from typing import List
import ast
from utils import (
    IGNORED_BUGS,
    generate_contextual_diff_with_char_limit,
    print_in_red,
    print_in_yellow,
)


def extract_function_with_imports(src: str, func_name: str) -> str:
    # Parsing the source code into an AST
    tree = ast.parse(src)

    # Find the function node and import statements
    function_node = None
    import_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            function_node = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_statements.append(node)

    if not function_node:
        return "Function not found"

    # Get the source code of the function's signature
    start_line = function_node.lineno - 1
    end_line = (
        function_node.body[0].lineno - 2
    )  # The line before the function body starts
    function_signature = "\n".join(src.splitlines()[start_line : end_line + 1])

    # Get the function body
    function_body_lines = src.splitlines()[
        function_node.body[0].lineno - 1 : function_node.end_lineno
    ]

    # Determine the minimum indentation in the function body
    min_indent = min(
        (
            len(line) - len(line.lstrip())
            for line in function_body_lines
            if line.strip()
        ),
        default=0,
    )

    indent_spaces = " " * 4

    # Adjust the indentation for the function body
    function_body = "\n".join(
        indent_spaces + line[min_indent:] for line in function_body_lines
    )

    # Extract import statements as source code with appropriate indentation
    imports_code = "\n".join(
        indent_spaces + ast.get_source_segment(src, node) for node in import_statements
    )

    # Combine the function signature, imports, and function body
    modified_function = (
        function_signature.lstrip() + "\n" + imports_code + "\n" + function_body
    )

    return modified_function


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
        "2.2.3": "variable runtime value",
        "2.2.4": "variable runtime type",
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

        # angelic variables
        self._resolve_angelic_variables(buggy_function_info)

    def _resolve_angelic_variables(self, function_info):
        self.facts["2.2.3"] = []  # value
        self.facts["2.2.4"] = []  # type

        if (
            function_info.get("variable_values") is None
            or function_info.get("angelic_variable_values") is None
        ):
            print_in_yellow(
                "WARNING: variable_values or angelic_variable_values is empty"
            )
            return

        buggy_variables_values = function_info["variable_values"]
        angelic_variable_values = function_info["angelic_variable_values"]
        if len(buggy_variables_values) == 0 or len(angelic_variable_values) == 0:
            print_in_yellow(
                "WARNING: variable_values or angelic_variable_values is empty"
            )
            return

        test_cases_containing_variable_values = []
        test_cases_containing_variable_types = []

        for buggy_IO_tuple, angelic_IO_tuple in zip(
            buggy_variables_values, angelic_variable_values
        ):
            # if the the buggy program crash, the IO tuple will be incomplete and we should ignore it
            if len(buggy_IO_tuple) < 2 or len(buggy_IO_tuple[1].keys()) == 0:
                continue
            if len(angelic_IO_tuple) < 2 or len(angelic_IO_tuple[1].keys()) == 0:
                continue

            variables_values = {
                "start": self._resolve_variable_values(
                    buggy_IO_tuple[0], angelic_IO_tuple[0]
                ),
                "end": self._resolve_variable_values(
                    buggy_IO_tuple[1], angelic_IO_tuple[1]
                ),
            }
            variables_types = {
                "start": self._resolve_variable_types(
                    buggy_IO_tuple[0], angelic_IO_tuple[0]
                ),
                "end": self._resolve_variable_types(
                    buggy_IO_tuple[1], angelic_IO_tuple[1]
                ),
            }

            if (
                len(variables_values["start"]) == 0
                or len(variables_values["end"]) == 0
                or len(variables_types["start"]) == 0
                or len(variables_types["end"]) == 0
            ):
                continue

            test_cases_containing_variable_values.append(variables_values)
            test_cases_containing_variable_types.append(variables_types)

        self.facts["2.2.3"] = test_cases_containing_variable_values
        self.facts["2.2.4"] = test_cases_containing_variable_types

    def _resolve_variable_values(self, buggy_variable_dict, angelic_variable_dict):
        values = []

        for buggy_variable_item, angelic_variable_item in zip(
            buggy_variable_dict.items(), angelic_variable_dict.items()
        ):
            if buggy_variable_item[0] != angelic_variable_item[0]:
                print_in_red("FATAL: the variable name does not match")

            varName = buggy_variable_item[0]
            buggy_variable_record = buggy_variable_item[1]
            angelic_variable_record = angelic_variable_item[1]
            buggy_value = buggy_variable_record["variable_value"]
            ground_truth_value = angelic_variable_record["variable_value"]

            if not (
                self._does_this_variable_record_contains_non_empty_value(
                    buggy_variable_record
                )
                and self._does_this_2_variable_records_actually_have_changes(
                    buggy_variable_record, angelic_variable_record
                )
            ):
                continue

            value_diff = generate_contextual_diff_with_char_limit(
                buggy_value, ground_truth_value
            )
            values.append(
                {"varName": varName, "value": ground_truth_value, "diff": value_diff}
            )

        return values

    def _resolve_variable_types(self, buggy_variable_dict, angelic_variable_dict):
        types = []

        for buggy_variable_item, angelic_variable_item in zip(
            buggy_variable_dict.items(), angelic_variable_dict.items()
        ):
            if buggy_variable_item[0] != angelic_variable_item[0]:
                print_in_red("FATAL: the variable name does not match")

            varName = buggy_variable_item[0]
            buggy_variable_record = buggy_variable_item[1]
            angelic_variable_record = angelic_variable_item[1]

            if self._does_this_variable_record_contains_non_empty_value(
                buggy_variable_record
            ) and self._does_this_2_variable_records_actually_have_changes(
                buggy_variable_record, angelic_variable_record
            ):
                types.append(
                    {
                        "varName": varName,
                        "varType": buggy_variable_record["variable_type"],
                    }
                )

        return types

    @staticmethod
    def _does_this_2_variable_records_actually_have_changes(
        buggy_variable_record, angelic_variable_record
    ):
        if (
            buggy_variable_record["variable_value"]
            == angelic_variable_record["variable_value"]
            and buggy_variable_record["variable_type"]
            == angelic_variable_record["variable_type"]
        ):
            return False
        return True

    @staticmethod
    def _does_this_variable_record_contains_non_empty_value(variable_record):
        if (
            variable_record["variable_value"] == "None"
            or variable_record["variable_type"] == "None"
            or Facts._matches_builtin_method(variable_record["variable_value"])
        ):
            return False
        return True

    @staticmethod
    def _matches_builtin_method(string):
        pattern = r"<([a-zA-Z\-]+) (?:[^>]+) at 0x[0-9a-f]+>"
        return bool(re.match(pattern, string))

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


def collect_facts(bugid: str, dir_path: str, flag_overwrite=False):
    if bugid in IGNORED_BUGS:
        print_in_red(f"WARNING: {bugid} is ignored")
        return

    full_bugdir_path = os.path.join(dir_path, "-".join(bugid.split(":")))
    if not os.path.exists(full_bugdir_path):
        os.makedirs(full_bugdir_path)

    bug_json_file = os.path.join(full_bugdir_path, "bug-data.json")

    if flag_overwrite or not os.path.exists(bug_json_file):
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
        with open(bug_json_file, "w") as f:
            json.dump(json_output, f, indent=4)

    else:
        with open(bug_json_file, "r") as f:
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


def format_json(obj):
    formatted_json = json.dumps(obj, indent=4)
    return formatted_json


def write_markdown_files(facts: Facts, output_dir: str):
    for fact_key, fact_content in facts.facts.items():
        fact_name = Facts.FACT_MAP[fact_key]
        if "code" in fact_name:
            fact_type = "python"
        else:
            fact_type = "text"

        if isinstance(fact_content, list) or isinstance(fact_content, dict):
            fact_content = format_json(fact_content)
            fact_type = "json"
        fact_content = f"```{fact_type}\n{fact_content}\n```\n"

        filename = "f" + fact_key.replace(".", "-") + ".md"
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(f"""# {fact_name}\n\n{fact_content}""")
