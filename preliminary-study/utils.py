IGNORED_BUGS = ["spacy:2"]


def print_in_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")
