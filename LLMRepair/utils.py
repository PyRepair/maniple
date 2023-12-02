import difflib
import ast


IGNORED_BUGS = ["spacy:2"]

FACT_MAP = {
    "1.1.1": "buggy function code",
    "1.1.2": "buggy function docstring",
    "1.2.1": "buggy class declearation",
    "1.2.2": "buggy class docstring",
    "1.2.3": "invoked method signature",
    "1.3.1": "buggy file name",
    "1.3.2": "invoked function signature",
    "2.1.1": "test function code",
    "2.1.2": "test file name",
    "2.2.1": "error message",
    "2.2.2": "stacktrace",
    "2.2.3": "angelic values",
    "2.2.4": "angelic types",
    "2.2.5": "buggy runtime values",
    "2.2.6": "buggy runtime types",
    "3.1.1": "issue title",
    "3.1.2": "issue description",
}


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")


def print_in_yellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")


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


def extract_function_from_response(src: str, func_name: str) -> str:
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
        return None

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
