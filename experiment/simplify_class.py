import argparse
import pyperclip
import ast
import astunparse


def read_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def read_from_clipboard():
    return pyperclip.paste()


class FilterMethodTransformer(ast.NodeTransformer):
    def __init__(self, method_name):
        self.method_name = method_name
        self.method_references = set()
        self.current_method_references = set()

    def collect_method_references(self, node):
        for n in ast.walk(node):
            if isinstance(n, ast.FunctionDef) and n.name == self.method_name:
                for subnode in ast.walk(n):
                    if (isinstance(subnode, ast.Attribute) and
                            isinstance(subnode.value, ast.Name) and subnode.value.id == 'self'):
                        self.method_references.add(subnode.attr)
                break

    def visit_ClassDef(self, node):
        new_body = []
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                self.current_method_references = set()
                self.visit(n)
                if self.current_method_references & self.method_references or n.name == self.method_name:
                    new_body.append(n)
        node.body = new_body
        return node

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            self.current_method_references.add(node.attr)
        return node


def main():
    parser = argparse.ArgumentParser(description="Modify Python source code.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--path', help="Path to the source file", type=str)
    group.add_argument('-c', '--clipboard', help="Read from clipboard", action='store_true')
    parser.add_argument('-m', '--method-name', help="Method name to focus on", required=True, type=str)

    args = parser.parse_args()

    if args.path:
        source_code = read_from_file(args.path)
    elif args.clipboard:
        source_code = read_from_clipboard()
    else:
        raise ValueError("Invalid arguments")

    # Parse the source code to produce the AST
    tree = ast.parse(source_code)

    # Transform the AST to collect references from the specified method
    transformer = FilterMethodTransformer(args.method_name)
    transformer.collect_method_references(tree)

    # Transform the AST to filter methods based on the collected references
    new_tree = transformer.visit(tree)

    # Convert the modified AST back to source code
    new_source_code = astunparse.unparse(new_tree)

    print(new_source_code)


if __name__ == "__main__":
    main()
