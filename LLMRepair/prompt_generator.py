import glob
import json
import os.path
import time
import re

import openai
import tiktoken
from openai import OpenAI
from typing import List, Optional
from utils import estimate_function_code_length, print_in_red, print_in_yellow

client = OpenAI(api_key="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")


class PromptGenerator:
    def __init__(self, facts: dict, facts_bitvector: dict, output_dir: str, remove_not_exist_facts: int) -> None:
        self.facts: dict = facts
        self.bitvector: dict = facts_bitvector.copy()
        self.output_dir: str = output_dir

        paths = output_dir.split("\\")
        parts = paths[-1].split("-")
        self.project_name = "-".join(parts[0: -1])
        self.bugid = parts[-1]

        with open("prompt_template.json", "r") as template_file:
            self.template: dict = json.load(template_file)
        self.prompt: str = ""

        with open(os.path.join(output_dir, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = next(iter(json.load(bug_data_file).values()))
            user_dir: str = list(bug_data)[0]
            self.buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]

        self.remove_not_exist_facts = remove_not_exist_facts

        self.actual_bitvector = facts_bitvector.copy()
        for key in self.bitvector.keys():
            if key == "cot":
                continue

            if self.bitvector[key] == 1 and self.facts[key] is None:
                self.actual_bitvector[key] = 0

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

        if self.actual_bitvector["2.2.5"] == 0 and self.actual_bitvector["2.2.6"] == 0:
            return

        self.prompt = self.prompt + "# Variable runtime "

        if self.actual_bitvector["2.2.5"] == 1 and self.actual_bitvector["2.2.6"] == 1:
            self.prompt = self.prompt + "value and type"
        elif self.actual_bitvector["2.2.5"] == 1:
            self.prompt = self.prompt + "value"
        elif self.actual_bitvector["2.2.6"] == 1:
            self.prompt = self.prompt + "type"

        self.prompt = self.prompt + " inside buggy function\n"

        for test_case_index in range(len(variable_runtime_value_test_cases)):
            self.prompt = self.prompt + f"## Buggy case {test_case_index + 1}\n"

            runtime_values: list = variable_runtime_value_test_cases[test_case_index]
            runtime_types: list = variable_runtime_type_test_cases[test_case_index]

            self.prompt = self.prompt + "### input parameter runtime "
            if self.actual_bitvector["2.2.5"] == 1 and self.actual_bitvector["2.2.6"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.actual_bitvector["2.2.5"] == 1:
                self.prompt = self.prompt + "value"
            elif self.actual_bitvector["2.2.6"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + " for buggy function\n"

            input_parameter_values: dict = runtime_values[0]
            input_parameter_types: dict = runtime_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.actual_bitvector["2.2.5"] == 1 and self.actual_bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                elif self.actual_bitvector["2.2.5"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.actual_bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + f"type: `{variable_type}`"

                self.prompt = self.prompt + "\n\n"

            variable_values_before_return: dict = runtime_values[1]
            variable_types_before_return: dict = runtime_types[1]

            if len(variable_values_before_return) == 0:
                self.prompt = self.prompt + "Variable runtime info is not available due to buggy function crashed \n\n"

            else:
                self.prompt = self.prompt + "### variable runtime "
                if self.actual_bitvector["2.2.5"] == 1 and self.actual_bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + "value and type"
                elif self.actual_bitvector["2.2.5"] == 1:
                    self.prompt = self.prompt + "value"
                elif self.actual_bitvector["2.2.6"] == 1:
                    self.prompt = self.prompt + "type"

                self.prompt = self.prompt + " before buggy function return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]
                    variable_type = variable_types_before_return[variable]

                    self.prompt = self.prompt + f"{variable}, "

                    if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                    elif self.actual_bitvector["2.2.3"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`"
                    elif self.actual_bitvector["2.2.4"] == 1:
                        self.prompt = self.prompt + f"type: `{variable_type}`"

                    self.prompt = self.prompt + "\n\n"

    def generate_variable_angelic_info(self):
        variable_angelic_value_test_cases: list = self.facts["2.2.3"]
        variable_angelic_type_test_cases: list = self.facts["2.2.4"]

        if self.actual_bitvector["2.2.3"] == 0 and self.actual_bitvector["2.2.4"] == 0:
            return

        self.prompt = self.prompt + "# Expected variable "

        if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
            self.prompt = self.prompt + "value and type"
        elif self.actual_bitvector["2.2.3"] == 1:
            self.prompt = self.prompt + "value"
        elif self.actual_bitvector["2.2.4"] == 1:
            self.prompt = self.prompt + "type"

        self.prompt = self.prompt + " in tests\n"

        for test_case_index in range(len(variable_angelic_value_test_cases)):
            self.prompt = self.prompt + f"## Expected case {test_case_index + 1}\n"

            angelic_values: list = variable_angelic_value_test_cases[test_case_index]
            angelic_types: list = variable_angelic_type_test_cases[test_case_index]

            self.prompt = self.prompt + "### Input parameter "
            if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.actual_bitvector["2.2.3"] == 1:
                self.prompt = self.prompt + "value"
            elif self.actual_bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + "\n"

            input_parameter_values: dict = angelic_values[0]
            input_parameter_types: dict = angelic_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                elif self.actual_bitvector["2.2.3"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.actual_bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"type: `{variable_type}`"

                self.prompt = self.prompt + "\n\n"

            self.prompt = self.prompt + "### Expected variable "
            if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "value and type"
            elif self.actual_bitvector["2.2.3"] == 1:
                self.prompt = self.prompt + "value"
            elif self.actual_bitvector["2.2.4"] == 1:
                self.prompt = self.prompt + "type"

            self.prompt = self.prompt + " before function return\n"

            variable_values_before_return: dict = angelic_values[1]
            variable_types_before_return: dict = angelic_types[1]
            for variable in variable_values_before_return.keys():
                variable_value = variable_values_before_return[variable]
                variable_type = variable_types_before_return[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.actual_bitvector["2.2.3"] == 1 and self.actual_bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"expected value: `{variable_value}`, type: `{variable_type}`"
                elif self.actual_bitvector["2.2.3"] == 1:
                    self.prompt = self.prompt + f"expected value: `{variable_value}`"
                elif self.actual_bitvector["2.2.4"] == 1:
                    self.prompt = self.prompt + f"expected type: `{variable_type}`"

                self.prompt = self.prompt + "\n\n"

    def generate_cot(self):
        if self.actual_bitvector["cot"] == 1:
            self.prompt = self.prompt + self.template["cot"]

    def generate_issue_section(self):
        issue_titles = self.facts["3.1.1"]
        issue_descriptions = self.facts["3.1.2"]

        if issue_titles is None and issue_descriptions is None:
            return

        if issue_titles is not None:
            issue_length = len(issue_titles)
        else:
            issue_length = len(issue_descriptions)

        for issue_index in range(issue_length):
            if self.actual_bitvector["3.1.1"] == 1:
                self.prompt = self.prompt + self.template["3.1.1"] + "```text\n"
                self.prompt = self.prompt + issue_titles[issue_index] + "```"
                self.add_newline_between_sections()

            if self.actual_bitvector["3.1.2"] == 1:
                self.prompt = self.prompt + self.template["3.1.2"] + "```text\n"
                self.prompt = self.prompt + issue_descriptions[issue_index] + "```\n"

            self.prompt = self.prompt + "\n"

    def generate_test_related_section(self):
        for test_index in range(len(self.facts["2.1.1"])):
            if self.actual_bitvector["2.1.1"] == 1:
                self.prompt = self.prompt + self.template["2.1.1"] + "```python\n"

                if self.actual_bitvector["2.1.2"] == 1:
                    self.prompt = self.prompt + self.template["2.1.2"] + self.facts["2.1.2"][test_index]
                    self.add_newline_between_sections()

                self.prompt = self.prompt + self.facts["2.1.1"][test_index] + "\n```"
                self.add_newline_between_sections()

            error_messages = self.facts["2.2.1"][test_index]
            stack_traces = self.facts["2.2.2"][test_index]

            if self.actual_bitvector["2.2.1"] == 1 and self.actual_bitvector["2.2.2"] == 1:
                self.prompt = self.prompt + self.template["2.2.1"] + "```text\n"
                for error_index in range(len(stack_traces)):
                    self.prompt = self.prompt + stack_traces[error_index] + "\n"
                    if error_index < len(error_messages):
                        self.prompt = self.prompt + error_messages[error_index] + "\n"

                self.prompt = self.prompt + "\n```"

            else:
                if self.actual_bitvector["2.2.2"] == 1:
                    self.prompt = self.prompt + self.template["2.2.2"] + "```text\n"
                    for error_index in range(len(stack_traces)):
                        self.prompt = self.prompt + stack_traces[error_index] + "\n"

                    self.prompt = self.prompt + "\n```"

                if self.actual_bitvector["2.2.1"] == 1:
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

        if self.actual_bitvector["1.3.1"] == 1:
            self.prompt = self.prompt + self.template["1.3.1"] + self.facts["1.3.1"]
            self.add_newline_between_sections()

        if self.actual_bitvector["1.3.2"] == 1:
            has_function_in_file = True
            buggy_functions: List[str] = self.facts["1.3.2"]
            for function_index in range(len(buggy_functions)):
                self.prompt = self.prompt + self.template["1.3.2"]
                self.prompt = self.prompt + "def " + buggy_functions[function_index] + ":\n    " + omitted_code + "\n"
                self.prompt = self.prompt + "    pass"
                self.add_newline_between_sections()

        if self.actual_bitvector["1.2.1"] == 1:
            has_class_declaration = True
            self.prompt = self.prompt + self.template["1.2.1"]
            self.prompt = self.prompt + self.facts["1.2.1"] + ":\n"

            if self.actual_bitvector["1.2.2"] == 1:
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

        if self.actual_bitvector["1.2.3"] == 1:
            buggy_functions: List[str] = self.facts["1.2.3"]
            for function_index in range(len(buggy_functions)):
                self.prompt = self.prompt + indent + self.template["1.2.3"]
                self.prompt = self.prompt + indent + "def " + buggy_functions[
                    function_index] + ":\n" + indent + "    " + omitted_code + "\n"
                self.prompt = self.prompt + indent + "    pass"
                self.add_newline_between_sections()

        if indent != "":
            self.add_newline_between_sections()

        self.prompt = self.prompt + indent + "# this is the buggy function you need to fix\n"

        source_code: str = self.facts["1.1.1"]
        for statement in source_code.split('\n'):
            self.prompt = self.prompt + indent + statement + "\n"

            if ("def " + self.buggy_function_name) in statement and self.actual_bitvector["1.1.2"] == 1:
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
        if self.remove_not_exist_facts == 1:
            for value in self.actual_bitvector.values():
                prompt_file_name = prompt_file_name + str(value)
        else:
            for value in self.bitvector.values():
                prompt_file_name = prompt_file_name + str(value)

        prompt_file_name += "prompt.md"
        with open(os.path.join(self.output_dir, prompt_file_name), "w") as output_file:
            output_file.write(self.prompt)

    def get_response_from_gpt(self, repeat_count: int, gpt_model: str):
        bitvector_flatten = ""

        if self.remove_not_exist_facts == 1:
            for value in self.actual_bitvector.values():
                bitvector_flatten = bitvector_flatten + str(value)
        else:
            for value in self.bitvector.values():
                bitvector_flatten = bitvector_flatten + str(value)

        buggy_function_length = estimate_function_code_length(self.facts["1.1.1"])

        for count in range(repeat_count):
            response_md_file_name = bitvector_flatten + "response(" + str(count) + ").md"

            # if os.path.exists(os.path.join(self.output_dir, response_md_file_name)):
            #     print(f"{response_md_file_name} already exists in directory {self.output_dir}")
            #     continue

            try:
                messages = [{"role": "user", "content": self.prompt}]
                valid_response = None

                max_generation_count = 4
                response = create_query(messages, gpt_model)
                while (((fix_patch := contain_valid_fix_patch(response, self.buggy_function_name)) is not None)
                       and max_generation_count > 0):

                    response = create_query(messages, gpt_model)
                    time.sleep(3)
                    max_generation_count -= 1

                conversation_response = response
                max_conversation_count = 5
                if fix_patch is not None:
                    messages = [
                        {"role": "user", "content": self.prompt},
                        {"role": "assistant", "content": response},
                        {"role": "user", "content": "Print the full code of the fixed function"},
                    ]

                    while (estimate_function_code_length(fix_patch) < 0.7 * buggy_function_length
                           and max_conversation_count > 0):
                        # if the fix patch is omitted

                        conversation_response = create_query(messages, gpt_model)
                        fix_patch = contain_valid_fix_patch(conversation_response, self.buggy_function_name)
                        max_conversation_count -= 1

                if max_generation_count == 0:
                    print_in_yellow(print(f"{response_md_file_name} in directory {self.output_dir} exceed max generation count"))
                elif max_conversation_count == 0:
                    print_in_yellow(f"{response_md_file_name} in directory {self.output_dir} exceed max conversation count, write omitted code")
                else:
                    print(f"write response to file {response_md_file_name} in directory {self.output_dir}")

                with open(os.path.join(self.output_dir, response_md_file_name), "w") as output_file:
                    if valid_response is not None:
                        output_file.write(conversation_response)
                    else:
                        output_file.write("")

            except Exception as error:
                error_str = str(error)
                with open(os.path.join(self.output_dir, response_md_file_name), "w") as output_file:
                    output_file.write(error_str)

                print_in_red(error_str)
                print(f"write response error to file {response_md_file_name} in directory {self.output_dir}")


class QueryException(Exception):
    pass


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def create_query(messages: list, gpt_model: str) -> str:
    for message in messages:
        num_tokens = num_tokens_from_string(message["content"], "cl100k_base")
        if num_tokens > 16385:
            raise QueryException(f"{num_tokens} exceed maximum 16385 token size")

    retry_max_count = 10
    while retry_max_count > 0:
        try:
            chat_completion = client.chat.completions.create(
                model=gpt_model,
                messages=messages
            )
            return chat_completion.choices[0].message.content

        except openai.RateLimitError as rate_limit_error:
            time.sleep(15)
            retry_max_count -= 1

    raise QueryException("Tried 10 times OpenAI rate limit query")


# used to check if there is ```python ``` code tag in the response
# and the code block must contain buggy function name to ensure gpt is not interrupted
def contain_valid_fix_patch(response: str, buggy_function_name: str) -> Optional[str]:
    code_block_pattern = r'```(?:python)?(.*?)```'
    code_blocks = re.findall(code_block_pattern, response, re.DOTALL)

    for code_block in code_blocks:
        if ("def " + buggy_function_name) in code_block:
            return code_block

    return None


if __name__ == "__main__":
    stratum = os.path.join("..", "preliminary-study", "first-stratum")
    remove_not_exist_facts = 0

    stratum_path = os.listdir(stratum)

    bitvectors = []

    pattern = "*bitvector*.json"
    bitvector_files = glob.glob(os.path.join("..", "preliminary-study", pattern))
    for file in bitvector_files:
        with open(file, "r") as input_bitvector_file:
            bitvectors.append(json.load(input_bitvector_file))

    for bitvector in bitvectors:
        for bug_dir in stratum_path:
            facts_path = os.path.join(stratum, bug_dir, "facts.json")
            if os.path.isfile(facts_path):
                with open(facts_path, "r") as input_file:
                    bug_facts = json.load(input_file)

                prompt_generator = PromptGenerator(bug_facts, bitvector, os.path.join(stratum, bug_dir), remove_not_exist_facts)
                prompt_generator.generate_prompt()
                prompt_generator.get_response_from_gpt(3, "gpt-3.5-turbo-1106")
                print(f"generate prompt for {bug_dir}")

            else:
                print(f"{bug_dir}: multi function fix, not supported")
