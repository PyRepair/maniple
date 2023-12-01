import difflib


IGNORED_BUGS = ["spacy:2"]


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
