import argparse
import glob
import json
import os.path
import threading
import pickle

from openai import OpenAI
from typing import List
from utils import print_in_red, print_in_yellow, divide_list
from gpt_utils import GPTConnection, QueryException, combine_token_usage

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
        for fact in facts.keys():
            bitvector[fact] = facts[fact]

    return bitvector


def get_strata_bitvector(strata_bitvector: dict) -> dict:
    bitvector = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0
    }
    for strata in strata_bitvector.keys():
        facts: dict = strata_bitvector[strata]
        for selected in facts.values():
            if selected == 1:
                bitvector[strata] = 1
                break

    return bitvector


class PromptGenerator:
    def __init__(self, database_dir: str, project_name: str, bug_id: str, strata_bitvector: dict) -> None:
        self.output_dir: str = os.path.join(database_dir, project_name, bug_id)

        facts_path = os.path.join(self.output_dir, "facts.json")
        if os.path.exists(facts_path):
            with open(facts_path, "r") as facts_file:
                self.facts: dict = json.load(facts_file)

            if self.facts["1.1.1"] is None:
                raise Exception(f"{project_name}:{bug_id} not single function fix, not supported")
        else:
            raise Exception(f"{project_name}:{bug_id} not single function fix, not supported")

        self.project_name = project_name
        self.bug_id = bug_id

        with open(os.path.join(os.path.dirname(__file__), "prompt_template.json"), "r") as template_file:
            self.template: dict = json.load(template_file)
        self.prompt: str = ""

        with open(os.path.join(self.output_dir, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = next(iter(json.load(bug_data_file).values()))
            user_dir: str = list(bug_data)[0]
            self.buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
            self.buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]
            self.buggy_function_source_code: str = bug_data[user_dir]["buggy_functions"][0]["function_code"]

            prefix = f"{project_name}_{bug_id}"
            start_idx = user_dir.find(prefix) + len(prefix) + 1
            self.buggy_location_file_name = user_dir[start_idx:]

        self.bitvector: dict = parse_bitvector_from_strata(strata_bitvector)
        self.actual_bitvector: dict = self.bitvector.copy()
        for key in self.bitvector.keys():
            if key == "cot":
                continue

            if self.bitvector[key] == 1 and self.facts[key] is None:
                self.actual_bitvector[key] = 0

        self.strata_bitvector: dict = get_strata_bitvector(strata_bitvector)
        self.actual_strata_bitvector: dict = self.get_actual_strata(strata_bitvector)

        self.strata_1_content = ""
        self.strata_2_content = ""
        self.strata_3_content = ""
        self.strata_4_content = ""
        self.strata_5_content = ""
        self.strata_6_content = ""
        self.strata_7_content = ""

        self.generate_prompt()

    def exist_null_strata(self):
        return self.strata_bitvector != self.actual_strata_bitvector

    def get_actual_strata(self, strata_bitvector: dict) -> dict:
        actual_strata_bitvector = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0
        }
        for strata in self.strata_bitvector.keys():
            if self.strata_bitvector[strata] == 1:
                facts: dict = strata_bitvector[strata]
                for fact in facts.keys():
                    if self.actual_bitvector[fact] == 1:
                        actual_strata_bitvector[strata] = 1
                        break

        return actual_strata_bitvector

    def generate_prompt(self):
        # self.prompt += f"The source code file is a member of the {self.project_name} repository.\n"

        self.prompt += self.template["preface"]
        self.add_newline_between_sections()

        self.generate_buggy_code_section()
        self.add_newline_between_sections()

        if self.actual_bitvector["2.1.5"] != 0 and self.actual_bitvector["2.1.6"] != 0:
            self.generate_variable_runtime_info()
            self.strata_5_content = self.strata_5_content + "\n\n"

        if self.actual_bitvector["2.1.3"] != 0 and self.actual_bitvector["2.1.4"] != 0:
            self.generate_variable_angelic_info()
            self.strata_5_content = self.strata_5_content + "\n\n"

        self.prompt = self.prompt + self.strata_5_content

        self.generate_test_related_section()
        self.add_newline_between_sections()

        if self.actual_bitvector["3.1.1"] != 0 and self.actual_bitvector["3.1.2"] != 0:
            self.generate_issue_section()
            self.add_newline_between_sections()

        self.generate_cot()

        self.collect_fact_content_in_prompt()

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

        self.strata_5_content = self.strata_5_content + f"# Runtime {place_holder} of variables inside the buggy function\n"

        self.strata_5_content = self.strata_5_content + f"Each case below includes input parameter {place_holder}, and the {place_holder} of relevant variables at the function's return, derived from executing failing tests. If an input parameter is not reflected in the output, it is assumed to remain unchanged. Note that some of these values at the function's return might be incorrect. Analyze these cases to identify why the tests are failing to effectively fix the bug.\n\n"

        for test_case_index in range(len(variable_runtime_value_test_cases)):
            self.strata_5_content = self.strata_5_content + f"## Case {test_case_index + 1}\n"

            runtime_values: list = variable_runtime_value_test_cases[test_case_index]
            runtime_types: list = variable_runtime_type_test_cases[test_case_index]

            self.strata_5_content = self.strata_5_content + f"### Runtime {place_holder} of the input parameters of the buggy function\n"

            input_parameter_values: dict = runtime_values[0]
            input_parameter_types: dict = runtime_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]["value"]
                variable_type = input_parameter_types[variable]
                if input_parameter_values[variable]["omitted"]:
                    variable_shape = f", shape: `{input_parameter_values[variable]['shape']}`"
                else:
                    variable_shape = ""

                self.strata_5_content = self.strata_5_content + f"{variable}, "

                if self.actual_bitvector["2.1.5"] == 1 and self.actual_bitvector["2.1.6"] == 1:
                    self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
                elif self.actual_bitvector["2.1.5"] == 1:
                    self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}"
                elif self.actual_bitvector["2.1.6"] == 1:
                    self.strata_5_content = self.strata_5_content + f"type: `{variable_type}`"

                self.strata_5_content = self.strata_5_content + "\n\n"

            variable_values_before_return: dict = runtime_values[1]
            variable_types_before_return: dict = runtime_types[1]
            if len(variable_values_before_return) > 0:
                self.strata_5_content = self.strata_5_content + f"### Runtime {place_holder} of variables right before the buggy function's return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]["value"]
                    variable_type = variable_types_before_return[variable]
                    if variable_values_before_return[variable]["omitted"]:
                        variable_shape = f", shape: `{variable_values_before_return[variable]['shape']}`"
                    else:
                        variable_shape = ""

                    self.strata_5_content = self.strata_5_content + f"{variable}, "

                    if self.actual_bitvector["2.1.5"] == 1 and self.actual_bitvector["2.1.6"] == 1:
                        self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
                    elif self.actual_bitvector["2.1.5"] == 1:
                        self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}"
                    elif self.actual_bitvector["2.1.6"] == 1:
                        self.strata_5_content = self.strata_5_content + f"type: `{variable_type}`"

                    self.strata_5_content = self.strata_5_content + "\n\n"

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

        self.strata_5_content = self.strata_5_content + f"# Expected {place_holder} of variables during the failing test execution\n"
        self.strata_5_content = self.strata_5_content + f"Each case below includes input parameter {place_holder}, and the expected {place_holder} of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.\n\n"

        for test_case_index in range(len(variable_angelic_value_test_cases)):
            self.strata_5_content = self.strata_5_content + f"## Expected case {test_case_index + 1}\n"

            angelic_values: list = variable_angelic_value_test_cases[test_case_index]
            angelic_types: list = variable_angelic_type_test_cases[test_case_index]

            self.strata_5_content = self.strata_5_content + f"### Input parameter {place_holder}\n"

            input_parameter_values: dict = angelic_values[0]
            input_parameter_types: dict = angelic_types[0]
            for variable in input_parameter_values.keys():
                variable_value = input_parameter_values[variable]["value"]
                variable_type = input_parameter_types[variable]
                if input_parameter_values[variable]["omitted"]:
                    variable_shape = f", shape: `{input_parameter_values[variable]['shape']}`"
                else:
                    variable_shape = ""

                self.strata_5_content = self.strata_5_content + f"{variable}, "

                if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
                    self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
                elif self.actual_bitvector["2.1.3"] == 1:
                    self.strata_5_content = self.strata_5_content + f"value: `{variable_value}`{variable_shape}"
                elif self.actual_bitvector["2.1.4"] == 1:
                    self.strata_5_content = self.strata_5_content + f"type: `{variable_type}`"

                self.strata_5_content = self.strata_5_content + "\n\n"

            variable_values_before_return: dict = angelic_values[1]
            variable_types_before_return: dict = angelic_types[1]
            if len(variable_values_before_return) > 0:
                self.strata_5_content = self.strata_5_content + f"### Expected {place_holder} of variables right before the buggy function's return\n"

                for variable in variable_values_before_return.keys():
                    variable_value = variable_values_before_return[variable]["value"]
                    variable_type = variable_types_before_return[variable]
                    if variable_values_before_return[variable]["omitted"]:
                        variable_shape = f", shape: `{variable_values_before_return[variable]['shape']}`"
                    else:
                        variable_shape = ""

                    self.strata_5_content = self.strata_5_content + f"{variable}, "

                    if self.actual_bitvector["2.1.3"] == 1 and self.actual_bitvector["2.1.4"] == 1:
                        self.strata_5_content = self.strata_5_content + f"expected value: `{variable_value}`{variable_shape}, type: `{variable_type}`"
                    elif self.actual_bitvector["2.1.3"] == 1:
                        self.strata_5_content = self.strata_5_content + f"expected value: `{variable_value}`{variable_shape}"
                    elif self.actual_bitvector["2.1.4"] == 1:
                        self.strata_5_content = self.strata_5_content + f"expected type: `{variable_type}`"

                    self.strata_5_content = self.strata_5_content + "\n\n"

    def generate_cot(self):
        if self.actual_bitvector["cot"] == 1:
            optional_1 = (f"{'buggy class, ' if self.actual_strata_bitvector['2'] == 1 else ''}"
                          f"{'related functions, ' if self.actual_strata_bitvector['3'] == 1 else ''}"
                          f"{'test code and corresponding error message, ' if self.actual_strata_bitvector['4'] == 1 else ''}"
                          f"{'the expected and actual input/output variable information, ' if self.actual_strata_bitvector['5'] == 1 else ''}"
                          f"{'the github issue' if self.actual_strata_bitvector['6'] == 1 else ''}")
            if optional_1[-3:-1] == ", ":
                optional_1 = optional_1[:-3] + optional_1[-1]

            new_line_str = "\n"

            count = 98
            optional_2 = ""
            if self.actual_strata_bitvector['2'] == 1:
                optional_2 += f"   ({chr(count)}). The buggy class\n"
                count += 1

            if self.actual_strata_bitvector['3'] == 1:
                optional_2 += f"   ({chr(count)}). The related functions\n"
                count += 1

            if self.actual_strata_bitvector['4'] == 1:
                optional_2 += f"   ({chr(count)}). The failing test and error message\n"
                count += 1

            if self.actual_strata_bitvector['5'] == 1:
                optional_2 += f"   ({chr(count)}). Discrepancies between expected and actual input/output variable value\n"
                count += 1

            if self.actual_strata_bitvector['6'] == 1:
                optional_2 += f"   ({chr(count)}). The GitHub Issue information\n"
                count += 1

            count = 97
            optional_3 = ""
            if self.actual_strata_bitvector['4'] == 1:
                optional_3 += f"   ({chr(count)}). Passes the failing test\n"
                count += 1

            if self.actual_strata_bitvector['5'] == 1:
                optional_3 += f"   ({chr(count)}). Satisfies the expected input/output variable information provided\n"
                count += 1

            if self.actual_strata_bitvector['6'] == 1:
                optional_3 += f"   ({chr(count)}). Successfully resolves the issue posted in GitHub\n"
                count += 1

            self.strata_7_content = self.strata_7_content + f"""{"1. Analyze the buggy function and it's relationship with the " + optional_1 + "." if optional_1 != "" else "1. Analyze the buggy function."}
2. Identify the potential error location within the problematic function.
3. Elucidate the bug's cause using:
   (a). The buggy function
{optional_2}
4. Suggest possible approaches for fixing the bug.
{'5. Present the corrected code for the problematic function such that it satisfied the following:' + new_line_str + optional_3 if optional_3 != "" else "5. Present the corrected code"}
"""

        self.prompt = self.prompt + self.strata_7_content

    def generate_issue_section(self):
        issue_titles = self.facts["3.1.1"]
        issue_descriptions = self.facts["3.1.2"]

        if issue_titles is not None:
            issue_length = len(issue_titles)
        else:
            issue_length = len(issue_descriptions)

        for issue_index in range(issue_length):
            if self.actual_bitvector["3.1.1"] == 1:
                self.strata_6_content = self.strata_6_content + self.template["3.1.1"] + "```text\n"
                self.strata_6_content = self.strata_6_content + issue_titles[issue_index] + "```"
                self.strata_6_content = self.strata_6_content + "\n\n"

            if self.actual_bitvector["3.1.2"] == 1:
                self.strata_6_content = self.strata_6_content + self.template["3.1.2"] + "```text\n"
                self.strata_6_content = self.strata_6_content + issue_descriptions[issue_index] + "```\n"

            self.strata_6_content = self.strata_6_content + "\n"

        self.prompt = self.prompt + self.strata_6_content

    def generate_test_related_section(self):
        for test_index in range(len(self.facts["1.4.1"])):
            if self.actual_bitvector["1.4.1"] == 1:
                self.strata_4_content = self.strata_4_content + self.template["1.4.1"] + "```python\n"

                if self.actual_bitvector["1.4.2"] == 1:
                    self.strata_4_content = self.strata_4_content + self.template["1.4.2"] + self.facts["1.4.2"][test_index]
                    self.strata_4_content = self.strata_4_content + "\n\n"

                self.strata_4_content = self.strata_4_content + self.facts["1.4.1"][test_index] + "\n```"
                self.strata_4_content = self.strata_4_content + "\n\n"

            if (self.actual_bitvector["2.1.1"] == 1 and self.actual_bitvector["2.1.2"] == 1 and
                    (self.facts["2.1.1"] is not None and self.facts["2.1.2"] is not None)):

                error_messages = self.facts["2.1.1"][test_index]
                stack_traces = self.facts["2.1.2"][test_index]

                self.strata_4_content = self.strata_4_content + self.template["2.1.1"] + "```text\n"
                for error_index in range(len(stack_traces)):
                    self.strata_4_content = self.strata_4_content + stack_traces[error_index] + "\n"
                    if error_index < len(error_messages):
                        self.strata_4_content = self.strata_4_content + error_messages[error_index] + "\n"

                self.strata_4_content = self.strata_4_content + "\n```"

            else:
                if self.actual_bitvector["2.1.2"] == 1 and (self.facts["2.1.2"] is not None):

                    stack_traces = self.facts["2.1.2"][test_index]

                    self.strata_4_content = self.strata_4_content + self.template["2.1.2"] + "```text\n"
                    for error_index in range(len(stack_traces)):
                        self.strata_4_content = self.strata_4_content + stack_traces[error_index] + "\n"

                    self.strata_4_content = self.strata_4_content + "\n```"

                if self.actual_bitvector["2.1.1"] == 1 and (self.facts["2.1.2"] is not None):

                    error_messages = self.facts["2.1.1"][test_index]

                    self.strata_4_content = self.strata_4_content + self.template["2.1.1"] + "```text\n"
                    for error_index in range(len(error_messages)):
                        self.strata_4_content = self.strata_4_content + error_messages[error_index] + "\n"

                    self.strata_4_content = self.strata_4_content + "\n```"

            self.strata_4_content = self.strata_4_content + "\n"

        self.prompt = self.prompt + self.strata_4_content

    def generate_buggy_code_section(self):
        self.prompt = self.prompt + self.template["1.1.1"]

        if not (self.facts["used_imports"] is None or self.facts["used_imports"] == [] or self.facts["used_imports"] == ""):
            self.prompt = self.prompt + "You can assume that the following imports are available in current environment and you don't need to import them again when generating fix patch.\n"
            self.prompt = self.prompt + "```python\n"
            self.prompt = self.prompt + self.facts["used_imports"]
            self.prompt = self.prompt + "\n```\n\n"

        self.prompt = self.prompt + "```python\n"

        ignore_comment = "# Please ignore the body of this function"
        has_function_in_file = False
        has_class_declaration = False

        if self.actual_bitvector["1.3.1"] == 1:
            self.strata_3_content = self.strata_3_content + self.template["1.3.1"] + self.facts["1.3.1"] + "\n\n"

        if self.actual_bitvector["1.3.2"] == 1:
            has_function_in_file = True
            buggy_functions: List[str] = self.facts["1.3.2"]
            for function_index in range(len(buggy_functions)):
                self.strata_3_content = self.strata_3_content + self.template["1.3.2"]
                self.strata_3_content = self.strata_3_content + "def " + buggy_functions[function_index] + ":\n    " + ignore_comment + "\n\n"

        self.prompt = self.prompt + self.strata_3_content

        if self.actual_bitvector["1.2.1"] == 1:
            has_class_declaration = True
            self.strata_2_content = self.strata_2_content + self.template["1.2.1"]
            self.strata_2_content = self.strata_2_content + self.facts["1.2.1"] + ":\n"

            if self.actual_bitvector["1.2.2"] == 1:
                class_docs: str = self.facts["1.2.2"]
                self.strata_2_content = self.strata_2_content + "    \"\"\"\n"
                for doc in class_docs.split('\n'):
                    self.strata_2_content = self.strata_2_content + "    " + doc + "\n"
                self.strata_2_content = self.strata_2_content + "    \"\"\""
                self.strata_2_content = self.strata_2_content + "\n\n"

            self.strata_2_content = self.strata_2_content + "\n\n"

        if (not has_function_in_file) and (not has_class_declaration):
            indent = ""
        elif has_function_in_file and (not has_class_declaration):
            indent = ""
        else:
            indent = "    "

        if self.actual_bitvector["1.2.3"] == 1:
            buggy_functions: List[str] = self.facts["1.2.3"]
            for function_index in range(len(buggy_functions)):
                self.strata_2_content = self.strata_2_content + indent + self.template["1.2.3"]
                self.strata_2_content = self.strata_2_content + indent + "def " + buggy_functions[function_index] + ":\n"
                self.strata_2_content = self.strata_2_content + indent + "    " + ignore_comment + "\n\n"

        self.prompt = self.prompt + self.strata_2_content

        if indent != "":
            self.add_newline_between_sections()

        self.prompt = self.prompt + indent + "# this is the buggy function you need to fix\n"

        source_code = ""
        if self.bitvector["1.1.1"] == 1 and self.bitvector["1.1.2"] == 1:
            source_code: str = self.buggy_function_source_code

        for statement in source_code.split('\n'):
            self.strata_1_content = self.strata_1_content + indent + statement + "\n"

        self.prompt = self.prompt + self.strata_1_content + "```"

    def add_newline_between_sections(self):
        self.prompt = self.prompt + "\n\n"

    def write_prompt(self):
        prompt_file_name = ""
        for value in self.bitvector.values():
            prompt_file_name = prompt_file_name + str(value)

        prompt_file_name += "_prompt.md"
        with open(os.path.join(self.output_dir, prompt_file_name), "w", encoding='utf-8') as output_file:
            output_file.write(self.prompt)

    def collect_fact_content_in_prompt(self):
        for selected in self.strata_bitvector.values():
            if selected == 0:
                return

        with open(os.path.join(self.output_dir, "facts-in-prompt.json"), "w") as prompt_facts_file:
            facts_content_strata = {
                "1": self.strata_1_content,
                "2": self.strata_2_content,
                "3": self.strata_3_content,
                "4": self.strata_4_content,
                "5": self.strata_5_content,
                "6": self.strata_6_content,
                "7": self.strata_7_content
            }

            json.dump(facts_content_strata, prompt_facts_file, indent=4)

    def generate_response(self, start_index: int, trial_number: int, gpt_model: str):
        bitvector_flatten = ""

        for value in self.bitvector.values():
            bitvector_flatten = bitvector_flatten + str(value)

        responses = None
        try:
            responses = GPTConnection().get_response_with_fix_path(self.prompt, gpt_model, trial_number, self.facts["1.1.1"], self.buggy_function_name)
        except QueryException as error:
            error_str = str(error)
            print_in_yellow(error_str)
        except Exception as error:
            error_str = str(error)
            print_in_red(error_str)

        for index in range(trial_number):
            file_index = index + start_index
            response_md_file_name = bitvector_flatten + "_response_" + str(file_index) + ".md"
            response_json_file_name = bitvector_flatten + "_response_" + str(file_index) + ".json"

            response_md_file_path = os.path.join(self.output_dir, response_md_file_name)
            response_json_file_path = os.path.join(self.output_dir, response_json_file_name)

            if responses is not None:
                response = responses["responses"][index]

                with open(response_md_file_path, "w", encoding='utf-8') as md_file:
                    md_file.write(response["response"])

                with open(response_json_file_path, "w", encoding='utf-8') as json_file:
                    test_input_data = {
                        self.project_name: [
                            {
                                "bugID": int(self.bug_id),
                                "bitvector": self.bitvector,
                                "strata": self.strata_bitvector,
                                "available_bitvector": self.actual_bitvector,
                                "available_strata": self.actual_strata_bitvector,
                                "start_line": self.buggy_function_start_line,
                                "file_name": self.buggy_location_file_name,
                                "replace_code": response["replace_code"],
                                "import_list": response["import_list"]
                            }
                        ]
                    }
                    json.dump(test_input_data, json_file, indent=4)

                print(f"write response to {response_md_file_path}")

            else:
                with open(response_md_file_path, "w", encoding='utf-8') as md_file:
                    md_file.write(error_str)

                with open(response_json_file_path, "w", encoding='utf-8') as json_file:
                    test_input_data = {
                        self.project_name: [
                            {
                                "bugID": int(self.bug_id),
                                "bitvector": self.bitvector,
                                "strata": self.strata_bitvector,
                                "available_bitvector": self.actual_bitvector,
                                "available_strata": self.actual_strata_bitvector,
                                "start_line": self.buggy_function_start_line,
                                "file_name": self.buggy_location_file_name,
                                "replace_code": None,
                                "import_list": []
                            }
                        ]
                    }
                    json.dump(test_input_data, json_file, indent=4)

                print_in_yellow(f"write response error to {response_md_file_path}")

        if responses is not None:
            completion_file_name = bitvector_flatten + "_completion" + ".pkl"
            completion_file_path = os.path.join(self.output_dir, completion_file_name)

            with open(completion_file_path, 'wb') as completion_file:
                pickle.dump((responses["prompt_messages"], responses["response_completions"]), completion_file)

            return responses["total_token_usage"]

        else:
            return {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }


def run_single_bitvector_partition(partition_bitvectors, start_index, trial_number):
    global total_token_usage

    for bitvector_strata in partition_bitvectors:
        for project in projects:
            project_folder_path = os.path.join(database_path, project)
            if not os.path.isdir(project_folder_path):
                continue

            for bid in os.listdir(project_folder_path):
                bug_dir_path = os.path.join(project_folder_path, bid)
                if not os.path.isdir(bug_dir_path):
                    continue

                prompt_generator = PromptGenerator(database_path, project, bid, bitvector_strata)
                if not prompt_generator.exist_null_strata():
                    prompt_generator.write_prompt()
                    # print(f"\ngenerate response for {project}:{bid}")
                    # token_usage = prompt_generator.generate_response(start_index, trial_number, "gpt-3.5-turbo-1106")
                    #
                    # with lock:
                    #     total_token_usage = combine_token_usage(total_token_usage, token_usage)

                # try:
                #     prompt_generator = PromptGenerator(database_path, project, bid, bitvector_strata)
                #     if not prompt_generator.exist_null_strata():
                #         prompt_generator.write_prompt()
                #         print(f"\ngenerate response for {project}:{bid}")
                #         token_usage = prompt_generator.generate_response(start_index, trial_number, "gpt-3.5-turbo-1106")
                #         total_token_usage = combine_token_usage(total_token_usage, token_usage)
                #
                # except Exception as e:
                #     print_in_red(str(e))


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--database",
        type=str,
        help="specify a database name under training-data folder",
        required=True
    )
    args_parser.add_argument(
        "--partition",
        type=int,
        help="how much partition you want, this will split dataset and run every partition parallel",
        required=True
    )
    args_parser.add_argument(
        "--start_index",
        type=int,
        help="The start index of file",
        required=True
    )
    args_parser.add_argument(
        "--trial",
        type=int,
        help="how many responses you want get from one prompt",
        required=True
    )

    args = args_parser.parse_args()

    database_path = os.path.join("training-data", args.database)
    projects = os.listdir(database_path)

    strata_bitvectors = []
    pattern = "*bitvector*.json"
    bitvector_files = glob.glob(os.path.join("experiment-initialization-resources", "strata-bitvectors", pattern))
    for file in bitvector_files:
        with open(file, "r") as input_bitvector_file:
            strata_bitvectors.append(json.load(input_bitvector_file))

    strata_bitvectors = divide_list(strata_bitvectors, args.partition)

    threads = []
    lock = threading.Lock()
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }

    for bitvector in strata_bitvectors:
        thread = threading.Thread(target=run_single_bitvector_partition, args=(bitvector, args.start_index, args.trial))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Total used token:")
    print(total_token_usage)
