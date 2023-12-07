import glob
import json
import os.path
import time
import re

import openai
import tiktoken
from openai import OpenAI
from typing import List, Optional
from utils import estimate_function_code_length, print_in_red, print_in_yellow, extract_function_from_response

client = OpenAI(api_key="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")


def parse_bitvector_from_strata(strata_bitvector: dict) -> dict:
    bitvector = {
        "1.1.1": 1,
        "1.1.2": 1,
        "1.2.1": 1,
        "1.2.2": 1,
        "1.2.3": 1,
        "1.3.1": 1,
        "1.3.2": 1,
        "1.4.1": 1,
        "1.4.2": 1,
        "2.1.1": 1,
        "2.1.2": 1,
        "2.1.3": 1,
        "2.1.4": 1,
        "2.1.5": 1,
        "2.1.6": 1,
        "3.1.1": 1,
        "3.1.2": 1,
        "cot": 1
    }

    for strata in strata_bitvector.keys():
        facts: dict = strata_bitvector[strata]

        for fact, selected in facts:
            bitvector[fact] = selected

    return bitvector


def get_strata_bitvector(strata_bitvector: dict):
    bitvector = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0
    }
    for strata in strata_bitvector.keys():
        facts: dict = strata_bitvector[strata]
        for selected in facts.values():
            if selected == 1:
                bitvector[strata] = 1
                break

    return bitvector


class PromptGenerator:
    def __init__(self, database_dir: str, project_name: str, bug_id: str, strata_bitvector: dict, remove_not_exist_fact_label: int) -> None:
        self.output_dir: str = os.path.join(database_dir, project_name, bug_id)

        facts_path = os.path.join(self.output_dir, "facts.json")
        if os.path.isfile(facts_path):
            with open(facts_path, "r") as facts_file:
                self.facts: dict = json.load(facts_file)

            if self.facts["1.1.1"] is None:
                raise Exception(f"{project}:{bug_id} not single function fix, not supported")

        self.project_name = project_name
        self.bug_id = bug_id

        with open("prompt_template.json", "r") as template_file:
            self.template: dict = json.load(template_file)
        self.prompt: str = ""

        with open(os.path.join(self.output_dir, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = next(iter(json.load(bug_data_file).values()))
            user_dir: str = list(bug_data)[0]
            self.buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
            self.buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]

            prefix = project_name + "/"
            start_idx = user_dir.find(prefix) + len(prefix)
            self.buggy_location_file_name = user_dir[start_idx:]

        self.remove_not_exist_fact_label = remove_not_exist_fact_label

        self.bitvector: dict = parse_bitvector_from_strata(strata_bitvector)
        self.actual_bitvector: dict = self.bitvector.copy()
        for key in self.bitvector.keys():
            if key == "cot":
                continue

            if self.bitvector[key] == 1 and self.facts[key] is None:
                self.actual_bitvector[key] = 0

        self.strata_bitvector: dict = get_strata_bitvector(strata_bitvector)
        self.actual_strata_bitvector: dict = self.get_actual_strata(strata_bitvector)

        self.max_generation_count = 10
        self.max_conversation_count = 5

    def get_actual_strata(self, strata_bitvector: dict) -> dict:
        bitvector = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0
        }
        for strata, selected in self.strata_bitvector:
            if selected == 1:
                facts: dict = strata_bitvector[strata]
                for fact in facts.keys():
                    if self.actual_bitvector[fact] == 1:
                        bitvector[strata] = 1
                        break

        return bitvector

    def generate_prompt(self):
        self.prompt: str = self.template["preface"]
        self.add_newline_between_sections()

        self.generate_buggy_code_section()
        self.add_newline_between_sections()

        if self.actual_bitvector["2.1.5"] != 0 and self.actual_bitvector["2.1.6"] != 0:
            self.generate_variable_runtime_info()
            self.add_newline_between_sections()

        if self.actual_bitvector["2.1.3"] != 0 and self.actual_bitvector["2.1.4"] != 0:
            self.generate_variable_angelic_info()
            self.add_newline_between_sections()

        self.generate_test_related_section()
        self.add_newline_between_sections()

        if self.actual_bitvector["3.1.1"] != 0 and self.actual_bitvector["3.1.2"] != 0:
            self.generate_issue_section()
            self.add_newline_between_sections()

        self.generate_cot()

        self.write_prompt()

    def generate_variable_runtime_info(self):
        variable_runtime_value_test_cases: list = self.facts["2.1.5"]
        variable_runtime_type_test_cases: list = self.facts["2.1.6"]

        place_holder = ""
        if self.actual_bitvector["2.1.5"] == 1 and self.actual_bitvector["2.1.6"] == 1:
            place_holder = "value and type"
        elif self.actual_bitvector["2.1.5"] == 1:
            place_holder = "value"
        elif self.actual_bitvector["2.1.6"] == 1:
            place_holder = "type"

        self.prompt = self.prompt + f"# Variable runtime {place_holder} inside buggy function\n"

        for test_case_index in range(len(variable_runtime_value_test_cases)):
            self.prompt = self.prompt + f"## Buggy case {test_case_index + 1}\n"

            runtime_values: list = variable_runtime_value_test_cases[test_case_index]
            runtime_types: list = variable_runtime_type_test_cases[test_case_index]

            self.prompt = self.prompt + f"### input parameter runtime {place_holder} for buggy function\n"

            input_parameter_values: dict = runtime_values[0]
            input_parameter_types: dict = runtime_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.actual_bitvector["2.1.5"] == 1 and self.actual_bitvector["2.1.6"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                elif self.actual_bitvector["2.1.5"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.actual_bitvector["2.1.6"] == 1:
                    self.prompt = self.prompt + f"type: `{variable_type}`"

                self.prompt = self.prompt + "\n\n"

            variable_values_before_return: dict = runtime_values[1]
            variable_types_before_return: dict = runtime_types[1]
            if len(variable_values_before_return) == 0:
                self.prompt = self.prompt + "### Variable runtime info before function return is not available due to buggy function crashed\n\n"

            else:
                self.prompt = self.prompt + f"### variable runtime {place_holder} before buggy function return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]
                    variable_type = variable_types_before_return[variable]

                    self.prompt = self.prompt + f"{variable}, "

                    if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                    elif self.actual_bitvector["2.1.3"] == 1:
                        self.prompt = self.prompt + f"value: `{variable_value}`"
                    elif self.actual_bitvector["2.1.4"] == 1:
                        self.prompt = self.prompt + f"type: `{variable_type}`"

                    self.prompt = self.prompt + "\n\n"

    def generate_variable_angelic_info(self):
        variable_angelic_value_test_cases: list = self.facts["2.1.3"]
        variable_angelic_type_test_cases: list = self.facts["2.1.4"]

        place_holder = ""
        if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
            place_holder = "value and type"
        elif self.actual_bitvector["2.1.3"] == 1:
            place_holder = "value"
        elif self.actual_bitvector["2.1.4"] == 1:
            place_holder = "type"

        self.prompt = self.prompt + f"# Expected variable {place_holder} in tests\n"

        for test_case_index in range(len(variable_angelic_value_test_cases)):
            self.prompt = self.prompt + f"## Expected case {test_case_index + 1}\n"

            angelic_values: list = variable_angelic_value_test_cases[test_case_index]
            angelic_types: list = variable_angelic_type_test_cases[test_case_index]

            self.prompt = self.prompt + f"### Input parameter {place_holder}\n"

            input_parameter_values: dict = angelic_values[0]
            input_parameter_types: dict = angelic_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]
                variable_type = input_parameter_types[variable]

                self.prompt = self.prompt + f"{variable}, "

                if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`, type: `{variable_type}`"
                elif self.actual_bitvector["2.1.3"] == 1:
                    self.prompt = self.prompt + f"value: `{variable_value}`"
                elif self.actual_bitvector["2.1.4"] == 1:
                    self.prompt = self.prompt + f"type: `{variable_type}`"

                self.prompt = self.prompt + "\n\n"

            variable_values_before_return: dict = angelic_values[1]
            variable_types_before_return: dict = angelic_types[1]
            if len(variable_values_before_return) == 0:
                self.prompt = self.prompt + "### Expected variable value before function return is not available due to function crashed\n\n"

            else:
                self.prompt = self.prompt + f"### Expected variable {place_holder} before function return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]
                    variable_type = variable_types_before_return[variable]

                    self.prompt = self.prompt + f"{variable}, "

                    if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
                        self.prompt = self.prompt + f"expected value: `{variable_value}`, type: `{variable_type}`"
                    elif self.actual_bitvector["2.1.3"] == 1:
                        self.prompt = self.prompt + f"expected value: `{variable_value}`"
                    elif self.actual_bitvector["2.1.4"] == 1:
                        self.prompt = self.prompt + f"expected type: `{variable_type}`"

                    self.prompt = self.prompt + "\n\n"

    def generate_cot(self):
        if self.actual_bitvector["cot"] == 1:
            self.prompt = self.prompt + self.template["cot"]

    def generate_issue_section(self):
        issue_titles = self.facts["3.1.1"]
        issue_descriptions = self.facts["3.1.2"]

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
        for test_index in range(len(self.facts["1.4.1"])):
            if self.actual_bitvector["1.4.1"] == 1:
                self.prompt = self.prompt + self.template["1.4.1"] + "```python\n"

                if self.actual_bitvector["1.4.2"] == 1:
                    self.prompt = self.prompt + self.template["1.4.2"] + self.facts["1.4.2"][test_index]
                    self.add_newline_between_sections()

                self.prompt = self.prompt + self.facts["1.4.1"][test_index] + "\n```"
                self.add_newline_between_sections()

            error_messages = self.facts["2.1.1"][test_index]
            stack_traces = self.facts["2.1.2"][test_index]

            if self.actual_bitvector["2.1.1"] == 1 and self.actual_bitvector["2.1.2"] == 1:
                self.prompt = self.prompt + self.template["2.1.1"] + "```text\n"
                for error_index in range(len(stack_traces)):
                    self.prompt = self.prompt + stack_traces[error_index] + "\n"
                    if error_index < len(error_messages):
                        self.prompt = self.prompt + error_messages[error_index] + "\n"

                self.prompt = self.prompt + "\n```"

            else:
                if self.actual_bitvector["2.1.2"] == 1:
                    self.prompt = self.prompt + self.template["2.1.2"] + "```text\n"
                    for error_index in range(len(stack_traces)):
                        self.prompt = self.prompt + stack_traces[error_index] + "\n"

                    self.prompt = self.prompt + "\n```"

                if self.actual_bitvector["2.1.1"] == 1:
                    self.prompt = self.prompt + self.template["2.1.1"] + "```text\n"
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
        if self.remove_not_exist_fact_label == 1:
            for value in self.actual_bitvector.values():
                prompt_file_name = prompt_file_name + str(value)
        else:
            for value in self.bitvector.values():
                prompt_file_name = prompt_file_name + str(value)

        prompt_file_name += "_prompt.md"
        with open(os.path.join(self.output_dir, prompt_file_name), "w", encoding='utf-8') as output_file:
            output_file.write(self.prompt)

    def get_response_from_gpt(self, count_number: int, gpt_model: str):
        if self.remove_not_exist_fact_label == 1:
            bitvector = self.actual_bitvector.copy()
            strata = self.actual_strata_bitvector.copy()
        else:
            bitvector = self.bitvector.copy()
            strata = self.strata_bitvector.copy()

        bitvector_flatten = ""

        for value in bitvector.values():
            bitvector_flatten = bitvector_flatten + str(value)

        response_md_file_name = bitvector_flatten + "_response_" + str(count_number) + ".md"
        response_json_file_name = bitvector_flatten + "_response_" + str(count_number) + ".json"

        if os.path.exists(os.path.join(self.output_dir, response_md_file_name)):
            print(f"{response_md_file_name} already exists in directory {self.output_dir}")
            return

        try:
            buggy_function_length = estimate_function_code_length(self.facts["1.1.1"])
            self.max_generation_count = 10
            self.max_conversation_count = 5
            messages = [{"role": "user", "content": self.prompt}]

            response, fix_patch = self.get_response_with_valid_patch(messages, gpt_model)

            conversation_response = response

            messages = [
                {"role": "user", "content": self.prompt},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "Print the full code of the fixed function"},
            ]

            while (estimate_function_code_length(fix_patch) < 0.6 * buggy_function_length
                   and extract_function_from_response(response, self.buggy_function_name) is not None
                   and self.max_conversation_count > 0):
                # if the fix patch is omitted

                conversation_response, fix_patch = self.get_response_with_valid_patch(messages, gpt_model)
                self.max_conversation_count -= 1

            print(f"write response to file {response_md_file_name} in directory {self.output_dir}")

            with open(os.path.join(self.output_dir, response_md_file_name), "w") as md_file:
                md_file.write(conversation_response)

            with open(os.path.join(self.output_dir, response_json_file_name), "w") as json_file:
                test_input_data = {
                    self.project_name: [
                        {
                            "bugID": int(self.bug_id),
                            "bitvector": bitvector,
                            "strata": strata,
                            "start_line": self.buggy_function_start_line,
                            "file_name": self.buggy_location_file_name,
                            "replace_code": extract_function_from_response(response, self.buggy_function_name),
                        }
                    ]
                }
                json.dump(test_input_data, json_file, indent=4)

        except Exception as error:
            error_str = ""
            if self.max_generation_count == 0:
                print_in_yellow(print(f"{self.output_dir}/{response_md_file_name} "
                                      f"exceed max generation count"))
            elif self.max_conversation_count == 0:
                print_in_yellow(f"{self.output_dir}/{response_md_file_name} "
                                f"exceed max conversation count")
            else:
                error_str = str(error)
                print_in_red(error_str)

            with open(os.path.join(self.output_dir, response_md_file_name), "w") as md_file:
                md_file.write(error_str)

            print(f"write response error to file {self.output_dir}/{response_md_file_name}")

    def get_response_with_valid_patch(self, messages: list, gpt_model: str):
        while self.max_generation_count > 0:
            response = create_query(messages, gpt_model)
            fix_patch = contain_valid_fix_patch(response, self.buggy_function_name)
            if fix_patch is not None:
                return response, fix_patch

            self.max_generation_count -= 1

        raise QueryException("exceed max generation count")


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
            time.sleep(3)
            chat_completion = client.chat.completions.create(
                model=gpt_model,
                messages=messages
            )
            finish_reason = chat_completion.choices[0].finish_reason
            if finish_reason != "stop":
                print_in_yellow(f"retrying due to not stop, finish reason: {finish_reason}")
                
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
    stratum_path = os.path.join("..", "preliminary-study", "second-stratum")
    remove_not_exist_fact_label = 0

    projects = os.listdir(stratum_path)

    strata_bitvectors = []

    pattern = "*bitvector*.json"
    bitvector_files = glob.glob(os.path.join("..", "preliminary-study", pattern))
    for file in bitvector_files:
        with open(file, "r") as input_bitvector_file:
            strata_bitvectors.append(json.load(input_bitvector_file))

    for bitvector_strata in strata_bitvectors:
        for project in projects:
            bug_ids = os.listdir(os.path.join(stratum_path, project))
            for bid in bug_ids:
                try:
                    print(f"generate prompt for {project}")
                    prompt_generator = PromptGenerator(stratum_path, project, bid, bitvector_strata, remove_not_exist_fact_label)
                    prompt_generator.generate_prompt()
                    prompt_generator.get_response_from_gpt(3, "gpt-3.5-turbo-1106")
                except Exception as e:
                    print_in_red(str(e))
