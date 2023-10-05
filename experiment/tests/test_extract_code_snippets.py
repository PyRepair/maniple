import unittest
from experiment.llm_repair import extract_code_snippets  # Replace 'your_module' with the actual module name


class TestExtractCodeSnippets(unittest.TestCase):
    def test_single_code_block(self):
        markdown_content = """```python
def add(a, b):
    return a + b
```"""
        expected_output = "def add(a, b):\n    return a + b"
        self.assertEqual(expected_output, extract_code_snippets(markdown_content))

    def test_multiple_code_blocks(self):
        markdown_content = """```python
def add(a, b):
    return a + b
 ```

Some text in between.

```python
def subtract(a, b):
    return a - b
```

```python
def multiply(a, b):
    return a * b
```"""
        expected_output = ("def add(a, b):\n    return a + b\n"
                           "def subtract(a, b):\n    return a - b\n"
                           "def multiply(a, b):\n    return a * b")
        self.assertEqual(expected_output, extract_code_snippets(markdown_content))

    def test_no_code_blocks(self):
        markdown_content = "This is just regular text with no code blocks."
        expected_output = ""
        self.assertEqual(expected_output, extract_code_snippets(markdown_content))


if __name__ == "__main__":
    unittest.main()
