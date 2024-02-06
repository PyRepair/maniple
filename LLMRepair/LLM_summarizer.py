import json
import pickle
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any, List

import tiktoken

from features_extractor import Facts
from gpt_utils import get_responses_from_prompt, QueryException, get_and_save_response_with_fix_path
from utils import print_in_red, print_in_yellow, iter_bugid_folders, get_facts_in_prompt

total_usage = 0


# noinspection PyAttributeOutsideInit
class CustomFactProcessor(Facts):

    def _post_init(self):
        self.buggy_function_name = ""
        self.buggy_function_code = ""
        self.test_function_code = defaultdict[str, List[str]](list)
        self.test_function_code_text = ""
        self.error_message = ""

        # for validation
        self.project_name = self._bugid.split(":")[0]
        self.buggy_function_start_line = 0
        self.buggy_location_file_name = ""

        # begin processing
        with open(Path(self._bwd) / "bug-data.json") as f:
            json_data = json.load(f)
            self.load_from_json_object(json_data[self._bugid])

        self.facts_in_prompt = get_facts_in_prompt(Path(self._bwd))

    def get_bugid_folder(self):
        return Path(self._bwd)

    def get_test_case_section(self):
        prompts_sections = []
        for test_file_path, test_function_codes in self.test_function_code.items():
            section = ""
            section += f"The followings are test functions under directory `{test_file_path}` in the project.\n```python\n"
            section += "\n\n".join(test_function_codes)
            section += "\n```"
            prompts_sections.append(section)

        result = "\n\n".join(prompts_sections)
        result += f"\n\nThe error message that corresponds the the above test functions is:\n```\n{self.error_message}\n```"
        return result

    def get_test_function_prompt(self):
        # assign prompts
        result = self.get_test_case_section()

        instruction = Path("prompt_instructions/test_info_summarize.txt").read_text()
        prompt = f"{instruction}\n\n"
        prompt += "The following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += result

        return prompt

    def get_dynamic_values_section(self):
        runtime_variables_section = self.facts_in_prompt["5"].split("# Expected variable value and type in tests")
        if len(runtime_variables_section) >= 1:
            return runtime_variables_section[0].strip()
        else:
            return ""

    def get_dynamic_values_prompt(self):
        runtime_variables_section = self.get_dynamic_values_section()
        if runtime_variables_section == "":
            return ""
        instruction = Path("prompt_instructions/dynamic_value_summarize.txt").read_text()
        prompt = f"{instruction}\n\nThe following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += f"{runtime_variables_section}"
        return prompt

    def get_angelic_values_section(self):
        angelic_values_section = self.facts_in_prompt["5"].split("# Expected variable value and type in tests\n")
        if len(angelic_values_section) == 2:
            return "# Expected return value in tests\n" + angelic_values_section[1].strip()
        else:
            return ""

    def get_angelic_values_prompt(self):
        angelic_values_section = self.get_angelic_values_section()
        if angelic_values_section == "":
            return ""

        instruction = Path("prompt_instructions/angelic_value_summarize.txt").read_text()
        prompt = f"{instruction}\n\nThe following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += f"{angelic_values_section}"
        return prompt

    def get_github_issue_prompt(self):
        instruction = Path("prompt_instructions/github_issue_summarize.txt").read_text()
        github_issue_section = self.facts_in_prompt["6"]
        if github_issue_section == "":
            return ""
        prompt = f"{instruction}\n\n{github_issue_section}"
        return prompt

    def _resolve_buggy_function_code(self, buggy_function):
        self.buggy_function_code = buggy_function

    def _resolve_test_function_and_test_file_path(self, test_data):
        test_function_code = test_data["test_function_code"]
        test_file_path = self._remove_project_root(test_data["test_path"])
        self.test_function_code[test_file_path].append(textwrap.dedent(test_function_code))

    def _resolve_error_message_and_stacktrace(self, test_data):
        self.error_message = test_data["full_test_error"]

    def _resolve_buggy_function_start_line(self, lineno: int):
        self.buggy_function_start_line = lineno

    def _resolve_buggy_location_file_name(self, file_name: str):
        self.buggy_location_file_name = file_name

    def _resolve_buggy_function_name(self, name: str):
        self.buggy_function_name = name


def count_tokens(prompt: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(prompt))


def construct_prompt(processor: CustomFactProcessor):
    prompt = "Please correct the malfunctioning function provided below by using the relevant information listed to address this bug. Then, produce a revised version of the function that resolves the issue. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function."
    prompt += "\n\n"

    used_imports = processor.facts["used_imports"]
    if bool(used_imports):
        prompt += f"Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.\n```python\n{used_imports}\n```"

    prompt += "\n\n"
    prompt += f"The following is the buggy function that you need to fix:\n```python\n{processor.buggy_function_code}```"

    used_functions = processor.facts_in_prompt["2"]
    if used_functions != "":
        print("Preserving used functions. Tokens:", count_tokens(used_functions))
        prompt += "\n\n\n\n"
        prompt += f"## Functions Used in the Buggy Function\n```python{used_functions}```"
    else:
        print_in_red("No used functions")

    prompt = resolve_test_case(processor, prompt)

    prompt = resolve_runtime_value(processor, prompt)

    prompt = resolve_angelic_value(processor, prompt)

    prompt = resolve_github_issue(processor, prompt)

    cot_technique_instruction = processor.facts_in_prompt["7"]
    prompt += "\n\n\n\n"
    prompt += cot_technique_instruction

    return prompt


def resolve_test_case(processor, prompt):
    test_info_prompt = processor.get_test_function_prompt()
    if test_info_prompt == "":
        print_in_red("No test info")
        return prompt

    num_tokens = count_tokens(test_info_prompt)
    if num_tokens > 16_000:
        print_in_red(f"Test info summary is too long. Tokens: {num_tokens}")
        return prompt

    if num_tokens < 1000:
        print("Preserving test info. Tokens:", num_tokens)
        prompt += "\n\n\n\n"
        prompt += processor.get_test_case_section()
        return prompt

    print("Generating test info. Tokens:", count_tokens(test_info_prompt), end=" ")
    error_message_summary = get_response_and_store_results(prompt=test_info_prompt,
                                                           prompt_file=processor.get_bugid_folder() / "test_info_prompt.md",
                                                           response_file=processor.get_bugid_folder() / "test_info_response.md",
                                                           pkl_file=processor.get_bugid_folder() / "test_info_response.pkl")[0]
    print("->", count_tokens(error_message_summary))
    prompt += "\n\n\n\n"
    prompt += f"## Test Case Summary\n{error_message_summary}"
    return prompt


def resolve_runtime_value(processor, prompt):
    runtime_value_prompt = processor.get_dynamic_values_prompt()
    if runtime_value_prompt == "":
        print_in_red("No runtime value")
        return prompt

    num_tokens = count_tokens(runtime_value_prompt)
    if num_tokens > 16_000:
        print_in_red(f"Runtime value summary is too long. Tokens: {num_tokens}")
        return prompt

    if num_tokens < 1000:
        print("Preserving runtime value. Tokens:", num_tokens)
        prompt += "\n\n\n\n"
        prompt += processor.get_dynamic_values_section()
        return prompt

    print("Generating runtime value summary. Tokens:", num_tokens, end=" ")
    runtime_value_summary = get_response_and_store_results(prompt=runtime_value_prompt,
                                                           prompt_file=processor.get_bugid_folder() / "runtime_info_prompt.md",
                                                           response_file=processor.get_bugid_folder() / "runtime_info_response.md",
                                                           pkl_file=processor.get_bugid_folder() / "runtime_info_response.pkl")[0]
    print("->", count_tokens(runtime_value_summary))
    prompt += "\n\n\n\n"
    prompt += "## Summary of Runtime Variables and Types in the Buggy Function\n\n"
    prompt += runtime_value_summary

    return prompt


def resolve_angelic_value(processor, prompt):
    angelic_value_prompt = processor.get_angelic_values_prompt()
    if angelic_value_prompt == "":
        print_in_red("No angelic value")
        return prompt

    num_tokens = count_tokens(angelic_value_prompt)
    if num_tokens > 16_000:
        print_in_red(f"Angelic value summary is too long. Tokens: {num_tokens}")
        return prompt

    if num_tokens < 1000:
        print("Preserving angelic value. Tokens:", num_tokens)
        prompt += "\n\n\n\n"
        prompt += processor.get_angelic_values_section()
        return prompt

    print("Generating angelic value summary. Tokens:", num_tokens, end=" ")
    angelic_value_summary = get_response_and_store_results(prompt=angelic_value_prompt,
                                                           prompt_file=processor.get_bugid_folder() / "angelic_info_prompt.md",
                                                           response_file=processor.get_bugid_folder() / "angelic_info_response.md",
                                                           pkl_file=processor.get_bugid_folder() / "angelic_info_response.pkl")[0]
    print("->", count_tokens(angelic_value_summary))
    prompt += "\n\n\n\n"
    prompt += "## Summary of Expected Parameters and Return Values in the Buggy Function\n\n"
    prompt += angelic_value_summary

    return prompt


def resolve_github_issue(processor, prompt):
    github_issue_prompt = processor.get_github_issue_prompt()
    if github_issue_prompt == "":
        print_in_red("No GitHub issue")
        return prompt

    num_tokens = count_tokens(github_issue_prompt)
    if num_tokens > 16_000:
        print_in_red(f"GitHub issue summary is too long. Tokens: {num_tokens}")

    if num_tokens < 1000:
        print("Preserving GitHub issue. Tokens:", num_tokens)
        prompt += "\n\n\n\n"
        prompt += processor.facts_in_prompt["6"]
        return prompt

    print("Generating GitHub issue summary. Tokens:", num_tokens, end=" ")
    github_issue_summary = get_response_and_store_results(prompt=github_issue_prompt,
                                                          prompt_file=processor.get_bugid_folder() / "github_issue_prompt.md",
                                                          response_file=processor.get_bugid_folder() / "github_issue_response.md",
                                                          pkl_file=processor.get_bugid_folder() / "github_issue_response.pkl")[0]
    print("->", count_tokens(github_issue_summary))
    prompt += "\n\n\n\n"
    prompt += "## Summary of the GitHub Issue Related to the Bug\n\n"
    prompt += github_issue_summary

    return prompt


def get_response_and_store_results(prompt: str, prompt_file: Path, response_file: Path, pkl_file: Path, trials=1) -> List[str]:
    global total_usage

    # if this prompt is too long just set bit to 0
    # we need to estimate tokens first
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(prompt))
    if num_tokens > 16000:
        raise QueryException(f"Prompt is exceeding 16000 tokens")

    gpt_response = get_responses_from_prompt(
        prompt=prompt,
        model="gpt-3.5-turbo-1106",
        trial=trials,
        temperature=1
    )
    responses: List[str] = gpt_response["responses"]
    total_usage += gpt_response["total_token_usage"].total_tokens

    # prompt file
    prompt_file.write_text(prompt)

    # response file
    response_dir = response_file.parent
    response_filename = response_file.stem
    for i, response in enumerate(responses):
        file_with_suffix = response_dir / f"{response_filename}_{i + 1}.md"
        file_with_suffix.write_text(response)

    # pkl file
    with open(pkl_file, "wb") as dump_pickle_file:
        pickle.dump(responses, dump_pickle_file)

    return responses


def main():
    global total_usage

    database_folder_path = Path.cwd().parent / "training-data" / "summarize-experiment"

    for bugid, project_folder, bugid_folder in iter_bugid_folders(database_folder_path):
        print_in_yellow(f"Processing {bugid}...")

        facts_proc = CustomFactProcessor(bugid=bugid, bug_working_directory=bugid_folder)

        facts_proc.get_angelic_values_prompt()

        prompt = construct_prompt(facts_proc)
        with open(bugid_folder / "prompt.md", "w") as f:
            f.write(prompt)

        print("Generating patch response. Prompt tokens:", count_tokens(prompt))
        token_usage: Any = get_and_save_response_with_fix_path(prompt=prompt,
                                                               gpt_model="gpt-3.5-turbo-1106",
                                                               response_file_name_prefix="prompt_response",
                                                               database_dir=database_folder_path,
                                                               project_name=project_folder.name,
                                                               bug_id=bugid_folder.name,
                                                               trial=10)
        total_usage += token_usage.total_tokens

    print_in_yellow(f"Total token usage: {total_usage}, estimate {total_usage / 1000_000} dollars")


if __name__ == "__main__":
    main()
