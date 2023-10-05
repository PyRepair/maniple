import unittest
from experiment.llm_repair import remove_import_statement


class TestRemoveImportStatement(unittest.TestCase):
    def test_remove_single_import(self):
        input_code = ("import os\n\n"
                      "def add(a, b):\n"
                      "    return a + b")
        expected_output = ("def add(a, b):\n"
                           "    return a + b")
        self.assertEqual(remove_import_statement(input_code), expected_output)

    def test_remove_multiple_imports(self):
        input_code = ("import os\n"
                      "from os import path, makedirs\n"
                      "import math\n\n"
                      "def add(a, b):\n"
                      "    return a + b")
        expected_output = ("def add(a, b):\n"
                           "    return a + b")
        self.assertEqual(remove_import_statement(input_code), expected_output)

    def test_no_imports(self):
        input_code = ("def add(a, b):\n"
                      "    return a + b")
        expected_output = ("def add(a, b):\n"
                           "    return a + b")
        self.assertEqual(remove_import_statement(input_code), expected_output)

    def test_remove_imports_with_whitespace(self):
        input_code = ("  import os  \n"
                      "  from os import path, makedirs\n"
                      "  import math  \n\n"
                      "def add(a, b):\n"
                      "    return a + b")
        expected_output = ("def add(a, b):\n"
                           "    return a + b")
        self.assertEqual(remove_import_statement(input_code), expected_output)


if __name__ == '__main__':
    unittest.main()
