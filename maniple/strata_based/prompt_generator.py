import argparse
import copy
import glob
import json
import os.path
import threading
from pathlib import Path
import re

from openai import OpenAI
from typing import List
from maniple.utils.misc import print_in_red, print_in_yellow, divide_list
from maniple.utils.openai_utils import get_and_save_response_with_fix_path, combine_token_usage
from maniple.strata_based.prompt_template import generate_variable_angelic_info, generate_variable_runtime_info
from maniple.strata_based.fact_bitvector_generator import bitvector_map, strata_bitvector_map

client = OpenAI(api_key="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")


def parse_bitvector_from_strata_bitvector(strata_bitvector: dict) -> dict:
    bitvector = copy.deepcopy(bitvector_map)

    for strata in strata_bitvector.keys():
        facts: dict = strata_bitvector[strata]
        for fact in facts.keys():
            bitvector[fact] = facts[fact]

    return bitvector


def parse_strata_from_strata_bitvector(strata_bitvector: dict) -> dict:
    parsed_strata = {key: 0 for key in strata_bitvector_map}

    for strata in strata_bitvector.keys():
        facts: dict = strata_bitvector[strata]
        for selected in facts.values():
            if selected == 1:
                parsed_strata[strata] = 1
                break

    return parsed_strata


class PromptGenerator:
    def __init__(self, database_dir: str, project_name: str, bug_id: str, strata_bitvector: dict) -> None:
        self.database_dir = database_dir
        self.project_name = project_name
        self.bug_id = bug_id
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

        self.bitvector: dict = parse_bitvector_from_strata_bitvector(strata_bitvector)
        self.actual_bitvector: dict = copy.deepcopy(self.bitvector)
        for key in self.bitvector.keys():
            if key == "cot":
                continue

            if key == "1.3.3":
                if self.bitvector[key] == 1 and self.facts["used_imports"] is None:
                    self.actual_bitvector[key] = 0

            else:
                if self.bitvector[key] == 1 and self.facts[key] is None:
                    self.actual_bitvector[key] = 0

        self.strata_bitvector: dict = parse_strata_from_strata_bitvector(strata_bitvector)
        self.actual_strata_bitvector: dict = self.get_actual_strata(strata_bitvector)

        self.strata_1_content = ""
        self.strata_2_content = ""
        self.strata_3_content = ""
        self.strata_4_content = ""
        self.strata_5_content = ""
        self.strata_6_content = ""
        self.strata_7_content = ""
        self.strata_8_content = ""
        self.strata_9_content = ""

        self.generate_prompt()

    def exist_null_strata(self):
        return self.strata_bitvector != self.actual_strata_bitvector

    def get_actual_strata(self, strata_bitvector: dict) -> dict:
        actual_strata_bitvector = {key: 0 for key in strata_bitvector_map}

        for strata in self.strata_bitvector.keys():
            if self.strata_bitvector[strata] == 1:
                facts: dict = strata_bitvector[strata]
                for fact in facts.keys():
                    if self.actual_bitvector[fact] == 1:
                        actual_strata_bitvector[strata] = 1
                        break

        return actual_strata_bitvector

    def append_template(self, content: str, strata: int):
        self.prompt += content
        if strata == 1:
            self.strata_1_content += content
        elif strata == 2:
            self.strata_2_content += content
        elif strata == 3:
            self.strata_3_content += content
        elif strata == 4:
            self.strata_4_content += content
        elif strata == 5:
            self.strata_5_content += content
        elif strata == 6:
            self.strata_6_content += content
        elif strata == 7:
            self.strata_7_content += content
        elif strata == 8:
            self.strata_8_content += content
        elif strata == 9:
            self.strata_9_content += content

    def generate_prompt(self):
        self.prompt += self.template["preface"]
        if self.actual_bitvector["cot"] == 1:
            self.generate_cot()
        self.prompt += "\n\n"

        # source code section contains fix strata 1, optional strata 2, optional strata 3
        self.generate_buggy_code_section()
        self.prompt += "\n\n"

        self.generate_test_related_section()
        self.prompt += "\n\n"

        if self.actual_bitvector["2.1.5"] != 0 and self.actual_bitvector["2.1.6"] != 0:
            self.append_template(generate_variable_runtime_info(self.facts, self.actual_bitvector), 6)
            self.prompt += "\n\n"

        if self.actual_bitvector["2.1.3"] != 0 and self.actual_bitvector["2.1.4"] != 0:
            self.append_template(generate_variable_angelic_info(self.facts, self.actual_bitvector), 7)
            self.prompt += "\n\n"

        if self.actual_bitvector["3.1.1"] != 0 and self.actual_bitvector["3.1.2"] != 0:
            self.generate_issue_section()
            self.prompt += "\n\n"

    def generate_cot(self):
        if self.actual_bitvector["cot"] == 1:
            optional_1 = (f"{'buggy class, ' if self.actual_strata_bitvector['2'] == 1 else ''}"
                          f"{'related functions, ' if self.actual_strata_bitvector['3'] == 1 else ''}"
                          f"{'test code, ' if self.actual_strata_bitvector['4'] == 1 else ''}"
                          f"{'corresponding error message, ' if self.actual_strata_bitvector['5'] == 1 else ''}"
                          f"{'the runtime input/output values, ' if self.actual_strata_bitvector['6'] == 1 else ''}"
                          f"{'the expected input/output values, ' if self.actual_strata_bitvector['7'] == 1 else ''}"
                          f"{'the GitHub issue' if self.actual_strata_bitvector['8'] == 1 else ''}")
            if optional_1[-2:] == ", ":
                optional_1 = optional_1[:-2]

            new_line_str = "\n"

            optional_2 = "the buggy function, "
            if self.actual_strata_bitvector['2'] == 1 and self.actual_bitvector["1.2.2"] == 1:
                optional_2 += "the buggy class docs, "

            if self.actual_strata_bitvector['3'] == 1:
                optional_2 += "the related functions, "

            if self.actual_strata_bitvector['4'] == 1:
                optional_2 += "the failing test, "

            if self.actual_strata_bitvector['5'] == 1:
                optional_2 += "the corresponding error message, "

            if self.actual_strata_bitvector['6'] == 1:
                optional_2 += "the runtime input/output variable values, "

            if self.actual_strata_bitvector['7'] == 1:
                optional_2 += "the expected input/output variable values, "

            if self.actual_strata_bitvector['8'] == 1:
                optional_2 += "the GitHub Issue information"

            if optional_2[-2:] == ", ":
                optional_2 = optional_2[:-2]

            optional_3 = ""
            if self.actual_strata_bitvector['4'] == 1 or self.actual_strata_bitvector['5'] == 1:
                optional_3 += "pass the failing test, "

            if self.actual_strata_bitvector['7'] == 1:
                optional_3 += "satisfy the expected input/output values, "

            if self.actual_strata_bitvector['8'] == 1:
                optional_3 += "resolve the issue posted in GitHub"

            if optional_3[-2:] == ", ":
                optional_3 = optional_3[:-2]

            self.append_template(f"""Following these steps:
{"1. Analyze the buggy function and its relationship with " + optional_1 + "." if optional_1 != "" else "1. Analyze the buggy function."}
2. Identify potential error locations within the buggy function.
3. Explain the cause of the bug using {optional_2}.
4. Suggest a strategy for fixing the bug.
{f'5. Given the buggy function below, provide a corrected version. The corrected version should {optional_3}.' if optional_3 != "" else "5. Given the buggy function below, provide a corrected version."}
""", 9)

    def generate_issue_section(self):
        issue_titles = self.facts["3.1.1"]
        issue_descriptions = self.facts["3.1.2"]

        if issue_titles is not None:
            issue_length = len(issue_titles)
        else:
            issue_length = len(issue_descriptions)

        for issue_index in range(issue_length):
            self.append_template("## A GitHub issue for this bug\n\n", 8)

            if self.actual_bitvector["3.1.1"] == 1:
                self.append_template(self.template["3.1.1"] + "```text\n", 8)
                self.append_template(issue_titles[issue_index] + "```", 8)
                self.append_template("\n\n", 8)

            if self.actual_bitvector["3.1.2"] == 1:
                self.append_template(self.template["3.1.2"] + "```text\n", 8)
                self.append_template(issue_descriptions[issue_index] + "```\n", 8)

            self.append_template("\n", 8)

    def generate_test_related_section(self):
        for test_index in range(len(self.facts["1.4.1"])):
            if self.actual_bitvector["1.4.1"] == 1:
                self.append_template(self.template["1.4.1"] + "```python\n", 4)

                if self.actual_bitvector["1.4.2"] == 1:
                    self.append_template(self.template["1.4.2"] + self.facts["1.4.2"][test_index], 4)
                    self.append_template("\n\n", 4)

                self.append_template(self.facts["1.4.1"][test_index] + "\n```", 4)
                self.append_template("\n\n", 4)

            if (self.actual_bitvector["2.1.1"] == 1 and self.actual_bitvector["2.1.2"] == 1 and
                    (self.facts["2.1.1"] is not None and self.facts["2.1.2"] is not None)):

                error_messages = self.facts["2.1.1"][test_index]
                stack_traces = self.facts["2.1.2"][test_index]

                self.append_template(self.template["2.1.1"] + "```text\n", 5)
                for error_index in range(len(stack_traces)):
                    self.append_template(stack_traces[error_index] + "\n", 5)
                    if error_index < len(error_messages):
                        self.append_template(error_messages[error_index] + "\n", 5)

                self.append_template("\n```\n", 5)

            else:
                if self.actual_bitvector["2.1.2"] == 1 and (self.facts["2.1.2"] is not None):

                    stack_traces = self.facts["2.1.2"][test_index]

                    self.append_template(self.template["2.1.2"] + "```text\n", 5)
                    for error_index in range(len(stack_traces)):
                        self.append_template(stack_traces[error_index] + "\n", 5)

                    self.append_template("\n```\n", 5)

                if self.actual_bitvector["2.1.1"] == 1 and (self.facts["2.1.2"] is not None):

                    error_messages = self.facts["2.1.1"][test_index]

                    self.append_template(self.template["2.1.1"] + "```text\n", 5)
                    for error_index in range(len(error_messages)):
                        self.append_template(error_messages[error_index] + "\n", 5)

                    self.append_template("\n```\n", 5)

            self.append_template("\n", 4)

    def generate_buggy_code_section(self):
        if self.facts["used_imports"] is not None:
            self.append_template(self.template["1.3.3"], 1)
            self.append_template("```python\n", 1)
            self.append_template(self.facts["used_imports"], 1)
            self.append_template("\n```\n\n", 1)

        self.append_template(self.template["1.1.1"], 1)

        self.append_template("```python\n", 1)

        ignore_comment = "# Please ignore the body of this function"
        has_function_in_file = False
        has_class_declaration = False

        if self.actual_bitvector["1.3.1"] == 1:
            self.append_template(self.template["1.3.1"] + self.facts["1.3.1"] + "\n\n", 1)

        if self.actual_bitvector["1.3.2"] == 1:
            has_function_in_file = True
            buggy_functions: List[str] = self.facts["1.3.2"]
            for function_index in range(len(buggy_functions)):
                self.append_template(self.template["1.3.2"], 3)
                self.append_template("def " + buggy_functions[function_index] + ":\n    " + ignore_comment + "\n\n", 3)

        if self.actual_bitvector["1.2.1"] == 1:
            has_class_declaration = True

            self.append_template(self.template["1.2.1"], 2)
            self.append_template(self.facts["1.2.1"] + ":\n", 2)

            if self.actual_bitvector["1.2.2"] == 1:
                class_docs: str = self.facts["1.2.2"]

                self.append_template("    \"\"\"\n", 2)

                for doc in class_docs.split('\n'):
                    self.append_template("    " + doc + "\n", 2)

                self.append_template("    \"\"\"", 2)

            self.append_template("\n\n\n", 2)

        # Add class declaration if buggy class invoked method enabled
        if self.actual_strata_bitvector["3"] == 1 and self.actual_strata_bitvector["2"] == 0 and self.facts["1.2.3"] != None:
            has_class_declaration = True

            self.append_template(self.template["1.2.1"], 3)
            self.append_template(self.facts["1.2.1"] + ":\n", 3)

        if (not has_function_in_file) and (not has_class_declaration):
            indent = ""
        elif has_function_in_file and (not has_class_declaration):
            indent = ""
        else:
            indent = "    "

        if self.actual_bitvector["1.2.3"] == 1:
            buggy_functions: List[str] = self.facts["1.2.3"]
            for function_index in range(len(buggy_functions)):
                self.append_template(indent + self.template["1.2.3"], 3)
                self.append_template(indent + "def " + buggy_functions[function_index] + ":\n", 3)
                self.append_template(indent + "    " + ignore_comment + "\n\n", 3)

        if indent != "":
            self.append_template("\n\n", 1)

        self.append_template(indent + "# this is the buggy function you need to fix\n", 1)

        # if self.bitvector["1.1.1"] == 1 and self.bitvector["1.1.2"] == 1:

        source_code: str = self.buggy_function_source_code
        for statement in source_code.split('\n'):
            self.append_template(indent + statement + "\n", 1)

        self.append_template("```", 1)

    def generate_imports_body(self) -> str:
        text = ""
        if self.facts["used_imports"] is not None:
            text += self.template["1.3.3"]
            text += "```python\n"
            text += self.facts["used_imports"]
            text += "\n```\n\n"

        return text

    def generate_source_code_body(self) -> str:
        text = ""

        ignore_comment = "# Please ignore the body of this function"
        has_function_in_file = False
        has_class_declaration = False

        if self.actual_bitvector["1.3.2"] == 1:
            has_function_in_file = True
            buggy_functions: List[str] = self.facts["1.3.2"]
            for function_index in range(len(buggy_functions)):
                text += self.template["1.3.2"]
                text += "def " + buggy_functions[function_index] + ":\n    " + ignore_comment + "\n\n"

        if self.actual_bitvector["1.2.1"] == 1:
            has_class_declaration = True

            text += self.template["1.2.1"]
            text += self.facts["1.2.1"] + ":\n"

            if self.actual_bitvector["1.2.2"] == 1:
                class_docs: str = self.facts["1.2.2"]

                text += "    \"\"\"\n"

                for doc in class_docs.split('\n'):
                    text += "    " + doc + "\n"

                text += "    \"\"\""

            text += "\n\n\n"

        # Add class declaration if buggy class invoked method enabled
        if self.actual_strata_bitvector["3"] == 1 and self.actual_strata_bitvector["2"] == 0 and self.facts["1.2.3"] != None:
            has_class_declaration = True

            text += self.template["1.2.1"]
            text += self.facts["1.2.1"] + ":\n"

        if (not has_function_in_file) and (not has_class_declaration):
            indent = ""
        elif has_function_in_file and (not has_class_declaration):
            indent = ""
        else:
            indent = "    "

        if self.actual_bitvector["1.2.3"] == 1:
            buggy_functions: List[str] = self.facts["1.2.3"]
            for function_index in range(len(buggy_functions)):
                text += indent + self.template["1.2.3"]
                text += indent + "def " + buggy_functions[function_index] + ":\n"
                text += indent + "    " + ignore_comment + "\n\n"

        if indent != "":
            text += "\n\n"

        text += indent + "# this is the buggy function you need to fix\n"

        # if self.bitvector["1.1.1"] == 1 and self.bitvector["1.1.2"] == 1:

        source_code: str = self.buggy_function_source_code
        for statement in source_code.split('\n'):
            text += indent + statement + "\n"

        return text

    def write_prompt(self):
        bitvector_flatten = ""
        for value in self.actual_strata_bitvector.values():
            bitvector_flatten = bitvector_flatten + str(value)

        bitvector_path = os.path.join(self.output_dir, bitvector_flatten)
        if not os.path.exists(bitvector_path):
            os.makedirs(bitvector_path)

        with open(os.path.join(bitvector_path, "prompt.md"), "w", encoding='utf-8') as output_file:
            output_file.write(self.prompt)

    def collect_fact_content_in_prompt(self):
        for selected in self.strata_bitvector.values():
            if selected == 0:
                return

        source_code_pattern = r"# The source code of the buggy function\n```python\n(.*?)```"
        match = re.search(source_code_pattern, self.prompt, re.DOTALL)
        facts_content_strata = {
            "1": self.strata_1_content,
            "2": self.strata_2_content,
            "3": self.strata_3_content,
            "4": self.strata_4_content,
            "5": self.strata_5_content,
            "6": self.strata_6_content,
            "7": self.strata_7_content,
            "8": self.strata_8_content,
            "9": self.strata_9_content,
            "1.3.3": self.generate_imports_body(),
            "source_code_body": self.generate_source_code_body()
        }

        return facts_content_strata

    def generate_response(self, start_index: int, trial_number: int, gpt_model: str):
        bitvector_flatten = ""

        for value in self.actual_strata_bitvector.values():
            bitvector_flatten = bitvector_flatten + str(value)

        data_to_store = {
            "bitvector": self.bitvector,
            "strata": self.strata_bitvector,
            "available_bitvector": self.actual_bitvector,
            "available_strata": self.actual_strata_bitvector
        }

        return get_and_save_response_with_fix_path(self.prompt, gpt_model, bitvector_flatten, self.database_dir,
                                                   self.project_name, self.bug_id, trial_number, data_to_store)


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
                    print(f"\ngenerate response for {project}:{bid}")
                    token_usage = prompt_generator.generate_response(start_index, trial_number, "gpt-3.5-turbo-0125")

                    with lock:
                        total_token_usage = combine_token_usage(total_token_usage, token_usage)


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

    database_path = os.path.join("data", args.database)
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
