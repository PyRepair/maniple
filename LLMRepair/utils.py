import difflib
import ast
import json
import os
import re
from typing import Dict, Optional


IGNORED_BUGS = ["spacy:2", "spacy:3", "spacy:5"]


class NotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_fact_map() -> Dict[str, str]:
    with open(os.path.join(os.path.dirname(__file__), "fact_strata_table.json")) as f:
        fact_map: dict = json.load(f)
    facts = fact_map["facts"]
    del facts["cot"]
    return facts


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


def print_in_yellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")


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


def extract_function_from_code_block(code_block: str, func_name: str) -> Optional[str]:
    try:
        return _extract_function_from_code_block_impl(code_block, func_name)
    except Exception:
        return None


def _extract_function_from_code_block_impl(
    code_block: str, func_name: str
) -> Optional[str]:
    """
    code block: valid python source code
    func_name: name of the function to be extracted
    """

    # Parsing the source code into an AST
    tree = ast.parse(code_block)

    # Find the function node and import statements
    function_node = None
    import_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            function_node = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_statements.append(node)

    if not function_node:
        return None

    # Get the source code of the function's signature
    start_line = function_node.lineno - 1
    end_line = (
        function_node.body[0].lineno - 2
    )  # The line before the function body starts
    function_signature = "\n".join(code_block.splitlines()[start_line : end_line + 1])

    # Get the function body
    function_body_lines = code_block.splitlines()[
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
        indent_spaces + ast.get_source_segment(code_block, node) for node in import_statements  # type: ignore
    )  # type: ignore

    # Combine the function signature, imports, and function body
    modified_function = (
        function_signature.lstrip() + "\n" + imports_code + "\n" + function_body
    )

    return modified_function
