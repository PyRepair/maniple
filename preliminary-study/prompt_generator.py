import glob
import json
import os.path
import time
import re

import openai
from openai import OpenAI
from typing import List


client = OpenAI(api_key="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")


class PromptGenerator:
    def __init__(self, facts: dict, facts_bitvector: dict, output_dir: str) -> None:
        self.facts: dict = facts
        self.bitvector: dict = facts_bitvector
        self.output_dir: str = output_dir
        with open("prompt_template.json", "r") as template_file:
            self.template: dict = json.load(template_file)
        self.prompt: str = ""

        with open(os.path.join(output_dir, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = next(iter(json.load(bug_data_file).values()))
            user_dir: str = list(bug_data)[0]
            self.buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]

    def generate_prompt(self):
        self.prompt: str = self.template["preface"]
        self.add_newline_between_sections()

        self.generate_buggy_code_section()
        self.add_newline_between_sections()

        self.generate_variable_runtime_info()
        self.add_newline_between_sections()

        self.generate_variable_angelic_info()
        self.add_newline_between_sections()

        self.generate_test_related_section()
        self.add_newline_between_sections()

        self.generate_issue_section()
        self.add_newline_between_sections()

        self.generate_cot()

        self.write_prompt()

    def generate_variable_runtime_info(self):
        variable_runtime_value_test_cases: list = self.facts["2.2.5"]
        variable_runtime_type_test_cases: list = self.facts["2.2.6"]

        if len(variable_runtime_value_test_cases) == 0 and self.bitvector["2.2.5"] == 0 and self.bitvector["2.2.6"] == 0:
            return

        self.prompt = self.prompt + "# Variable runtime "

        if self.bitvector["2.2.5"] == 1 and self.bitvector["2.2.6"] == 1:
            self.prompt = self.prompt + "value and type"
        elif self.bitvector["2.2.5"] == 1:
            self.prompt = self.prompt + "value"
        elif self.bitvector["2.2.6"] == 1:
            self.prompt = self.prompt + "type"

        self.prompt = self.prompt + " inside buggy function\n"

        for test_case_index in range(len(variable_runtime_value_test_cases)):
            self.prompt = self.prompt + f"## Buggy case {test_case_index + 1}\n"

            runtime_values: list = variable_runtime_value_test_cases[test_case_index]
            runtime_types: list = variable_runtime_type_test_cases[test_case_index]

            self.prompt = self.prompt + "### input parameter runtime "
            if self.bitvector["2.2.5"] == 1 and self.bitvector["2.2.6"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.bitvector["2.2.5"] == 1:
                self.prompt = self.prompt + "value"
            elif self.bitvector["2.2.6"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + " for buggy function\n"

            input_parameter_values: dict = runtime_values[0]
            input_parameter_types: dict = runtime_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.bitvector["2.2.5"] == 1 and self.bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: {variable_type}"
                elif self.bitvector["2.2.5"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + f"type: {variable_type}"

                self.prompt = self.prompt + "\n\n"

            variable_values_before_return: dict = runtime_values[1]
            variable_types_before_return: dict = runtime_types[1]

            if len(variable_values_before_return) == 0:
                self.prompt = self.prompt + "Variable runtime info is not available due to buggy function crashed \n\n"

            else:
                self.prompt = self.prompt + "### variable runtime "
                if self.bitvector["2.2.5"] == 1 and self.bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + "value and type"
                elif self.bitvector["2.2.5"] == 1:
                    self.prompt = self.prompt + "value"
                elif self.bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + "type"

                self.prompt = self.prompt + " before buggy function return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]
                    variable_type = variable_types_before_return[variable]

                    self.prompt = self.prompt + f"{variable}, "

                    if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`, type: {variable_type}"
                    elif self.bitvector["2.2.3"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`"
                    elif self.bitvector["2.2.4"] == 1:
                        self.prompt = self.prompt + f"type: {variable_type}"

                    self.prompt = self.prompt + "\n\n"

    def generate_variable_angelic_info(self):
        variable_angelic_value_test_cases: list = self.facts["2.2.3"]
        variable_angelic_type_test_cases: list = self.facts["2.2.4"]

        if len(variable_angelic_value_test_cases) == 0 and self.bitvector["2.2.3"] == 0 and self.bitvector["2.2.4"] == 0:
            return

        self.prompt = self.prompt + "# Expected variable "

        if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
            self.prompt = self.prompt + "value and type"
        elif self.bitvector["2.2.3"] == 1:
            self.prompt = self.prompt + "value"
        elif self.bitvector["2.2.4"] == 1:
            self.prompt = self.prompt + "type"

        self.prompt = self.prompt + " in tests\n"

        for test_case_index in range(len(variable_angelic_value_test_cases)):
            self.prompt = self.prompt + f"## Expected case {test_case_index + 1}\n"

            angelic_values: list = variable_angelic_value_test_cases[test_case_index]
            angelic_types: list = variable_angelic_type_test_cases[test_case_index]

            self.prompt = self.prompt + "### Input parameter "
            if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.bitvector["2.2.3"] == 1:
                self.prompt = self.prompt + "value"
            elif self.bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + "\n"

            input_parameter_values: dict = angelic_values[0]
            input_parameter_types: dict = angelic_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: {variable_type}"
                elif self.bitvector["2.2.3"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"type: {variable_type}"

                self.prompt = self.prompt + "\n\n"

            self.prompt = self.prompt + "### Expected variable "
            if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.bitvector["2.2.3"] == 1:
                self.prompt = self.prompt + "value"
            elif self.bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + " before function return\n"

            variable_values_before_return: dict = angelic_values[1]
            variable_types_before_return: dict = angelic_types[1]
            for variable in variable_values_before_return.keys():
                variable_value = variable_values_before_return[variable]
                variable_type = variable_types_before_return[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.bitvector["2.2.3"] == 1 and self.bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"expected value: `{variable_value}`, type: {variable_type}"
                elif self.bitvector["2.2.3"] == 1:
                    self.prompt = self.prompt + f"expected value: `{variable_value}`"
                elif self.bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"expected type: {variable_type}"

                self.prompt = self.prompt + "\n\n"

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

                if self.bitvector["2.1.2"] == 1 and "2.1.2" in self.facts:
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

        omitted_code = "# ... omitted code ..."
        has_function_in_file = False
        has_class_declaration = False

        if "1.3.1" in self.facts and self.bitvector["1.3.1"] == 1:
            self.prompt = self.prompt + self.template["1.3.1"] + self.facts["1.3.1"]
            self.add_newline_between_sections()

        if "1.3.2" in self.facts and self.facts["1.3.2"] != [] and self.bitvector["1.3.2"] == 1:
            has_function_in_file = True
            buggy_functions: List[str] = self.facts["1.3.2"]
            for function_index in range(len(buggy_functions)):
                self.prompt = self.prompt + self.template["1.3.2"]
                self.prompt = self.prompt + "def " + buggy_functions[function_index] + ":\n    " + omitted_code + "\n"
                self.prompt = self.prompt + "    pass"
                self.add_newline_between_sections()

        if "1.2.1" in self.facts and self.bitvector["1.2.1"] == 1:
            has_class_declaration = True
            self.prompt = self.prompt + self.template["1.2.1"]
            self.prompt = self.prompt + self.facts["1.2.1"] + ":\n"

            if "1.2.2" in self.facts and self.bitvector["1.2.2"] == 1:
                class_docs: str = self.facts["1.2.2"]
                self.prompt = self.prompt + "    \"\"\"\n"
                for doc in class_docs.split('\n'):
                    self.prompt = self.prompt + "    " + doc + "\n"
                self.prompt = self.prompt + "    \"\"\""
                self.add_newline_between_sections()

            self.prompt = self.prompt + "    " + omitted_code + "\n"
            self.add_newline_between_sections()

        if (not has_function_in_file) and (not has_class_declaration):
            indent = ""
        else:
            indent = "    "

        if "1.2.3" in self.facts and self.facts["1.2.3"] != [] and self.bitvector["1.2.3"] == 1:
            buggy_functions: List[str] = self.facts["1.2.3"]
            for function_index in range(len(buggy_functions)):
                self.prompt = self.prompt + indent + self.template["1.2.3"]
                self.prompt = self.prompt + indent + "def " + buggy_functions[function_index] + ":\n" + indent + "    " + omitted_code + "\n"
                self.prompt = self.prompt + indent + "    pass"
                self.add_newline_between_sections()

        if indent != "":
            self.add_newline_between_sections()

        self.prompt = self.prompt + indent + "# this is the buggy function you need to fix\n"

        source_code: str = self.facts["1.1.1"]
        for statement in source_code.split('\n'):
            self.prompt = self.prompt + indent + statement + "\n"

            if ("def " + self.buggy_function_name) in statement and "1.1.2" in self.facts and self.bitvector["1.1.2"] == 1:
                buggy_function_docs = self.facts["1.1.2"]

                self.prompt = self.prompt + indent + "    \"\"\"\n"
                for doc in buggy_function_docs.split('\n'):
                    self.prompt = self.prompt + indent + "    " + doc + "\n"

                self.prompt = self.prompt + indent + "    \"\"\"\n\n"

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
                try:
                    response: str = ""
                    max_generation_count = 5
                    while max_generation_count > 0:
                        chat_completion = client.chat.completions.create(
                            model=gpt_model,
                            messages=[
                                {"role": "user", "content": self.prompt}
                            ]
                        )

                        response = chat_completion.choices[0].message.content

                        if self.contain_valid_fix_patch(response, self.buggy_function_name):
                            break
                        else:
                            time.sleep(3)
                            response = chat_completion.choices[0].message.content
                            max_generation_count -= 1

                    if max_generation_count == 0:
                        print(f"write response error to file {response_file_name} in directory {self.output_dir}")
                    else:
                        print(f"write response to file {response_file_name} in directory {self.output_dir}")

                    with open(os.path.join(self.output_dir, response_file_name), "w") as output_file:
                        output_file.write(response)

                except Exception as error:
                    with open(os.path.join(self.output_dir, response_file_name), "w") as output_file:
                        output_file.write(str(error))
                    print(f"write response error to file {response_file_name} in directory {self.output_dir}")

    # used to check if there is ```python ``` code tag in the response
    # and the code block must contain buggy function name to ensure gpt is not interrupted
    @staticmethod
    def contain_valid_fix_patch(response: str, buggy_function_name: str) -> bool:
        code_block_pattern = r'```(?:python)?(.*?)```'
        code_blocks = re.findall(code_block_pattern, response, re.DOTALL)

        for code_block in code_blocks:
            if ("def " + buggy_function_name) in code_block:
                return True

        return False


if __name__ == "__main__":
    stratum = "first-stratum"
    null_check = 0

    stratum_path = os.listdir(stratum)

    bitvectors = []

    current_directory = os.getcwd()
    pattern = "*bitvector*.json"
    bitvector_files = glob.glob(os.path.join(current_directory, pattern))
    for file in bitvector_files:
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
