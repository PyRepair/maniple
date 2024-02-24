import difflib
import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np


class NotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_fact_map() -> Dict[str, str]:
    with open(os.path.join(os.path.dirname(__file__), "fact_strata_table.json")) as f:
        fact_map: dict = json.load(f)
    facts = fact_map["facts"]
    del facts["cot"]
    return facts


def divide_list(lst: list, n_partitions: int):
    if n_partitions <= 0:
        raise ValueError("Number of partitions must be a positive integer")

    partition_size, remainder = divmod(len(lst), n_partitions)
    return [
        lst[
            i * partition_size
            + min(i, remainder) : (i + 1) * partition_size
            + min(i + 1, remainder)
        ]
        for i in range(n_partitions)
    ]


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


def print_in_yellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")


def print_in_green(text):
    green_start = "\033[92m"
    reset = "\033[0m"
    print(f"{green_start}{text}{reset}")


def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0

    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def iter_bugid_folders(path: Path):
    """
    Iterate over all bugid folders in the given path
    :param path: path to the folder containing the bugid folders
    :return: a list of tuples containing the bugid, project folder path and bugid folder path
    """
    result = []
    for project_folder in path.iterdir():
        if not project_folder.is_dir():
            continue
        for bugid_folder in project_folder.iterdir():
            if not bugid_folder.is_dir():
                continue
            result.append((f"{project_folder.name}:{bugid_folder.name}", project_folder, bugid_folder))
    return result


def remove_comments_and_docstrings(source):
    """
    Remove comments and docstrings from a Python source code string using regex.
    """

    # Remove single line comments
    source = re.sub(r"#.*", "", source)

    # Remove docstrings
    source = re.sub(
        r"(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")", "", source, flags=re.DOTALL
    )

    # Remove import lines
    source = re.sub(
        r"^\s*(import .*|from .* import .*)\s*$", "", source, flags=re.MULTILINE
    )

    # Remove new lines
    source = re.sub(r"\n+", " ", source)

    return source.strip()


def estimate_function_code_length(src: str) -> int:
    return len(remove_comments_and_docstrings(src))


def generate_contextual_diff_with_char_limit(text1, text2, context=1, char_limit=30):
    """
    Generates a unified diff between two texts, including some context lines,
    but limits the number of characters per line in the context.

    Args:
    text1 (str): The original text.
    text2 (str): The modified text.
    context (int): The number of context lines to include around the changes.
    char_limit (int): Maximum number of characters to include per line.

    Returns:
    str: The unified diff string, showing the changes with limited context.
    """
    # Split the texts into lines
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)

    # Truncate each line to the specified character limit
    lines1_truncated = [line[:char_limit] for line in lines1]
    lines2_truncated = [line[:char_limit] for line in lines2]

    # Generate the unified diff with specified context
    diff = difflib.unified_diff(
        lines1_truncated, lines2_truncated, lineterm="", n=context
    )

    # Filter out the ---, +++, and @@ lines
    filtered_diff = [
        line
        for line in diff
        if not (
            line.startswith("---") or line.startswith("+++") or line.startswith("@@")
        )
    ]

    # Join the diff lines into a single string
    return "\n".join(filtered_diff)


def find_patch_from_response(
    raw_response: str, buggy_function_name: str
) -> Optional[str]:
    """
    This function extract code block that contains buggy function from the response of OpenAI

    raw_response: response from OpenAI
    buggy_function_name: name of the buggy function
    """

    code_block_pattern = r"```(?:python\n)?(.*?)(?:\n)?```"
    function_pattern = rf".*def.*{buggy_function_name}.*"

    code_blocks = re.findall(code_block_pattern, raw_response, re.DOTALL)
    for code_block in code_blocks:
        if re.search(function_pattern, code_block, re.DOTALL):
            return code_block
    return None


def extract_function_and_imports_from_code_block(
    code_block: str, func_name: str
) -> Tuple[Optional[str], Optional[List[str]]]:
    try:
        return _extract_function_and_imports_from_code_block_impl(code_block, func_name)
    except Exception:
        return None, None


def _extract_function_and_imports_from_code_block_impl(
    code_block: str, func_name: str
) -> Tuple[Optional[str], List[str]]:
    """
    Extracts a function and its import statements from a source code block.

    :param code_block: valid python source code
    :param func_name: name of the function to be extracted
    :return: Tuple containing the function code and a list of import statements
    """

    # Parsing the source code into an AST
    tree = ast.parse(code_block)

    # Find the function node and import statements
    function_node = None
    import_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) and node.name == func_name:
            function_node = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_statements.append(node)

    if not function_node:
        return None, []

    # Extract the source code of the function
    function_code = ast.get_source_segment(code_block, function_node)  # type: ignore

    if function_code is None:
        return None, []

    # Extract import statements as source code
    imports_code: List[str] = [
        ast.get_source_segment(code_block, node) for node in import_statements  # type: ignore
    ]

    return function_code, imports_code


def get_function_code(bugid_folder: Path, bugid: str) -> str:
    with open(bugid_folder / "bug-data.json") as f:
        json_data = json.load(f)
        __tmp0 = list(json_data[bugid].values())[0]
        return __tmp0["buggy_functions"][0]["function_code"]


def get_facts_in_prompt(bugid_folder: Path) -> Dict[str, str]:
    with open(bugid_folder / "facts-in-prompt.json") as f:
        return json.load(f)


def get_import_statements(bugid_folder: Path) -> str:
    with open(bugid_folder / "facts.json") as f:
        json_data = json.load(f)
        return json_data["used_imports"]


def clear_features(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith("f") and not file.startswith("f3"):
                os.remove(os.path.join(root, file))


def clear_logs(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the filename starts with 'f'
            if "log" in file:
                os.remove(os.path.join(root, file))


def clear_prompts(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "prompt" in file:
                os.remove(os.path.join(root, file))


def clear_responses(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "response" in file:
                os.remove(os.path.join(root, file))


def clear_results(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "result" in file:
                os.remove(os.path.join(root, file))
