import glob
import json
import os.path

from extractor import Facts


fact_map = Facts.FACT_MAP


class PromptGenerator:
    def __init__(self, facts: dict, facts_bitvector: dict, output_dir: str) -> None:
        self.facts: dict = facts
        self.bitvector: dict = facts_bitvector
        self.output_dir: str = output_dir
        with open("prompt_template.json", "r") as template_file:
            self.template: dict = json.load(template_file)
        self.prompt: str = ""

    def generate_prompt(self):
        self.prompt: str = self.template["preface"]
        self.add_newline_between_sections()

        self.generate_buggy_code_section()
        self.add_newline_between_sections()

        self.generate_test_related_section()
        self.add_newline_between_sections()

        self.generate_issue_section()
        self.add_newline_between_sections()

        self.generate_cot()

        self.write_prompt()

    def generate_cot(self):
        if self.bitvector["cot"] == 1:
            self.prompt = self.prompt + self.template["cot"]

    def generate_issue_section(self):
        if "3.1.1" not in self.facts or "3.1.2" not in self.facts:
            return

        issue_titles = self.facts["3.1.1"]
        issue_descriptions = self.facts["3.1.2"]

        for issue_index in range(len(issue_titles)):
            if self.bitvector["3.1.1"] == 1:
                self.prompt = self.prompt + self.template["3.1.1"] + "```text\n"
                self.prompt = self.prompt + issue_titles[issue_index] + "```"
                self.add_newline_between_sections()

            if self.bitvector["3.1.2"] == 1:
                self.prompt = self.prompt + self.template["3.1.2"] + "```text\n"
                self.prompt = self.prompt + issue_descriptions[issue_index] + "```\n"

            self.prompt = self.prompt + "\n"

    def generate_test_related_section(self):
        for test_index in range(len(self.facts["2.1.1"])):
            if self.bitvector["2.1.1"] == 1:
                self.prompt = self.prompt + self.template["2.1.1"] + "```python\n"

                if self.bitvector["2.1.2"] == 1:
                    self.prompt = self.prompt + self.template["2.1.2"] + self.facts["2.1.2"][test_index]
                    self.add_newline_between_sections()

                self.prompt = self.prompt + self.facts["2.1.1"][test_index] + "\n```"
                self.add_newline_between_sections()

            error_messages = self.facts["2.2.1"][test_index]
            stack_traces = self.facts["2.2.2"][test_index]

            if self.bitvector["2.2.1"] == 1 and self.bitvector["2.2.2"] == 1:
                self.prompt = self.prompt + self.template["2.2.1"] + "```text\n"
                for error_index in range(len(stack_traces)):
                    self.prompt = self.prompt + stack_traces[error_index] + "\n"
                    if error_index < len(error_messages):
                        self.prompt = self.prompt + error_messages[error_index] + "\n"

                self.prompt = self.prompt + "\n```"

            else:
                if self.bitvector["2.2.2"] == 1:
                    self.prompt = self.prompt + self.template["2.2.2"] + "```text\n"
                    for error_index in range(len(stack_traces)):
                        self.prompt = self.prompt + stack_traces[error_index] + "\n"

                    self.prompt = self.prompt + "\n```"

                if self.bitvector["2.2.1"] == 1:
                    self.prompt = self.prompt + self.template["2.2.1"] + "```text\n"
                    for error_index in range(len(error_messages)):
                        self.prompt = self.prompt + error_messages[error_index] + "\n"

                    self.prompt = self.prompt + "\n```"

            self.prompt = self.prompt + "\n"

    def generate_buggy_code_section(self):
        self.prompt = self.prompt + self.template["1.1.1"]
        self.prompt = self.prompt + "```python\n"

        indent = ""
        omitted_code = "# ... omitted code ...\n\n"

        if "1.3.2" in self.facts and self.bitvector["1.3.2"] == 1:
            self.prompt = self.prompt + self.template["1.3.2"] + self.facts["1.3.2"]
            self.add_newline_between_sections()

        if "1.3.4" in self.facts and self.facts["1.3.4"] != [] and self.bitvector["1.3.4"] == 1:
            functions: list[str] = self.facts["1.3.4"]
            for function_index in range(len(functions)):
                self.prompt = self.prompt + self.template["1.3.4"]
                self.prompt = self.prompt + "def " + functions[function_index] + ":\n    " + omitted_code

        if "1.2.1" in self.facts and self.bitvector["1.2.1"] == 1:
            indent = "    "
            self.prompt = self.prompt + self.template["1.2.1"]
            self.prompt = self.prompt + self.facts["1.2.1"] + ":\n"
            self.prompt = self.prompt + indent + omitted_code

        if "1.2.4" in self.facts and self.facts["1.2.4"] != [] and self.bitvector["1.2.4"] == 1:
            indent = "    "
            functions: list[str] = self.facts["1.2.4"]
            for function_index in range(len(functions)):
                self.prompt = self.prompt + indent + self.template["1.2.4"]
                self.prompt = self.prompt + indent + "def " + functions[function_index] + ":\n" + indent + indent + omitted_code

        if indent != "":
            self.add_newline_between_sections()

        self.prompt = self.prompt + indent + "# this is the buggy function you need to fix\n"

        source_code: str = self.facts["1.1.1"]

        for statement in source_code.split('\n'):
            self.prompt = self.prompt + indent + statement + "\n"

        self.prompt = self.prompt + "```"

    def add_newline_between_sections(self):
        self.prompt = self.prompt + "\n"
        self.prompt = self.prompt + "\n"

    def write_prompt(self):
        prompt_file_name = ""
        for value in self.bitvector.values():
            prompt_file_name = prompt_file_name + str(value)
        prompt_file_name += "prompt.md"
        with open(os.path.join(self.output_dir, prompt_file_name), "w") as output_file:
            output_file.write(self.prompt)


if __name__ == "__main__":
    first_stratum_path = os.listdir("first-stratum")

    bitvectors = []

    current_directory = os.getcwd()
    pattern = "*bitvector*.json"
    json_files = glob.glob(os.path.join(current_directory, pattern))
    for file in json_files:
        with open(file, "r") as input_bitvector_file:
            bitvectors.append(json.load(input_bitvector_file))

    for bitvector in bitvectors:
        for bug_dir in first_stratum_path:
            with open(os.path.join("first-stratum", bug_dir, "facts.json"), "r") as input_file:
                bug_facts = json.load(input_file)

            prompt_generator = PromptGenerator(bug_facts, bitvector, os.path.join("first-stratum", bug_dir))
            prompt_generator.generate_prompt()
