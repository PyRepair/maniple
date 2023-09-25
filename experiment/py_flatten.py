import argparse
import pyperclip


def read_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def read_from_clipboard():
    return pyperclip.paste()


def main():
    parser = argparse.ArgumentParser(description="Flatten a Python source file or read from clipboard.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--path', help="Path to the source file", type=str)
    group.add_argument('-c', '--clipboard', help="Read text from clipboard", action='store_true')

    args = parser.parse_args()

    if args.path:
        source_code = read_from_file(args.path)
    elif args.clipboard:
        source_code = read_from_clipboard()
    else:
        raise Exception("Invalid arguments")

    # Remove leading and trailing white spaces and flatten the file
    source_code = source_code.strip()

    # Replace escape sequences for special characters
    source_code = source_code.replace("\n", "\\n").replace("\t", "\\t")

    # Replace four spaces used for indentation with "\\s"
    source_code = source_code.replace("    ", "\\s")

    print(source_code)


if __name__ == "__main__":
    main()
