import glob
import json
import os.path
import time
import re

import openai
from openai import OpenAI

from extractor import Facts


fact_map = Facts.FACT_MAP
client = OpenAI(api_key="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")


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

        omitted_code = "# ... omitted code ...\n\n"
        has_function_in_file = False
        has_class_declaration = False
        indent = ""

        if "1.3.2" in self.facts and self.bitvector["1.3.2"] == 1:
            self.prompt = self.prompt + self.template["1.3.2"] + self.facts["1.3.2"]
            self.add_newline_between_sections()

        if "1.3.4" in self.facts and self.facts["1.3.4"] != [] and self.bitvector["1.3.4"] == 1:
            has_function_in_file = True
            functions: list[str] = self.facts["1.3.4"]
            for function_index in range(len(functions)):
                self.prompt = self.prompt + self.template["1.3.4"]
                self.prompt = self.prompt + "def " + functions[function_index] + ":\n    " + omitted_code

        if "1.2.1" in self.facts and self.bitvector["1.2.1"] == 1:
            has_class_declaration = True
            self.prompt = self.prompt + self.template["1.2.1"]
            self.prompt = self.prompt + self.facts["1.2.1"] + ":\n"
            self.prompt = self.prompt + "    " + omitted_code

        if (not has_function_in_file) and (not has_class_declaration):
            indent = ""
        else:
            indent = "    "

        if "1.2.4" in self.facts and self.facts["1.2.4"] != [] and self.bitvector["1.2.4"] == 1:
            functions: list[str] = self.facts["1.2.4"]
            for function_index in range(len(functions)):
                self.prompt = self.prompt + indent + self.template["1.2.4"]
                self.prompt = self.prompt + indent + "def " + functions[function_index] + ":\n" + indent + "    " + omitted_code

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

    def get_response_from_gpt(self, repeat_count: int, gpt_model: str):
        for count in range(repeat_count):
            response_file_name = ""
            for value in self.bitvector.values():
                response_file_name = response_file_name + str(value)
            response_file_name += "response(" + str(count) + ").md"

            if os.path.exists(os.path.join(self.output_dir, response_file_name)):
                print(f"{response_file_name} already exists in directory {self.output_dir}")

            else:
                with open(os.path.join(self.output_dir, response_file_name), "w") as output_file:
                    try:
                        max_generation_count = 5
                        while max_generation_count > 0:
                            chat_completion = client.chat.completions.create(
                                model=gpt_model,
                                messages=[
                                    {"role": "user", "content": self.prompt}
                                ]
                            )

                            response = chat_completion.choices[0].message.content

                            if self.contain_valid_fix_patch(response):
                                break
                            else:
                                time.sleep(3)
                                response = chat_completion.choices[0].message.content
                                max_generation_count -= 1

                        output_file.write(response)
                        print(f"write response to file {response_file_name} in directory {self.output_dir}")
                    except Exception as e:
                        output_file.write(str(e))
                        print(f"write response error to file {response_file_name} in directory {self.output_dir}")

    # used to check if there is ```python ``` code tag in the response
    @staticmethod
    def contain_valid_fix_patch(response: str) -> bool:
        code_block_pattern = r'```(?:python)?(.*?)```'
        code_blocks = re.findall(code_block_pattern, response, re.DOTALL)
        if len(code_blocks) == 0:
            return False
        else:
            return True


if __name__ == "__main__":
    stratum = "first-stratum"

    stratum_path = os.listdir(stratum)

    bitvectors = []

    current_directory = os.getcwd()
    pattern = "*bitvector*.json"
    json_files = glob.glob(os.path.join(current_directory, pattern))
    for file in json_files:
        with open(file, "r") as input_bitvector_file:
            bitvectors.append(json.load(input_bitvector_file))

    for bitvector in bitvectors:
        for bug_dir in stratum_path:
            facts_path = os.path.join(stratum, bug_dir, "facts.json")
            if os.path.isfile(facts_path):
                with open(facts_path, "r") as input_file:
                    bug_facts = json.load(input_file)

                try:
                    prompt_generator = PromptGenerator(bug_facts, bitvector, os.path.join(stratum, bug_dir))
                    prompt_generator.generate_prompt()
                    # prompt_generator.get_response_from_gpt(3, "gpt-3.5-turbo-1106")
                    print(f"generate prompt for {bug_dir}")
                except KeyError as e:
                    print(f"{bug_dir}: buggy function code are not available, not supported")
            else:
                print(f"{bug_dir}: multi function fix, not supported")
