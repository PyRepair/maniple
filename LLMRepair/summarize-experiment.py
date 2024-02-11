import pickle
from pathlib import Path
from typing import Any, List, Dict

import tiktoken

from gpt_utils import get_responses_from_prompt, QueryException, get_and_save_response_with_fix_path
from utils import print_in_red, print_in_yellow, iter_bugid_folders

total_usage = 0


class Processor:
    def __init__(self, bug_folder: Path):
        self.bug_folder = bug_folder



def count_tokens(prompt: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(prompt))


def construct_prompt(facts_in_prompt: Dict[str, str]):
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
    if test_info_prompt == "":
        print_in_red("No test info")
        return prompt

    num_tokens = count_tokens(test_info_prompt)
    if num_tokens > 16_000:
        print_in_red(f"Test info summary is too long. Tokens: {num_tokens}")
        return prompt

    if num_tokens < 1000:
        print("Preserving test info. Tokens:", num_tokens)
        prompt += "\n\n"
        prompt += test_info_prompt
        return prompt

    instruction = Path()

    print("Generating test info. Tokens:", count_tokens(test_info_prompt), end=" ")
    error_message_summary = get_response_and_store_results(prompt=test_info_prompt,
                                                           prompt_file=processor.get_bugid_folder() / "test_info_prompt.md",
                                                           response_file=processor.get_bugid_folder() / "test_info_response.md",
                                                           pkl_file=processor.get_bugid_folder() / "test_info_response.pkl")[0]
    print("->", count_tokens(error_message_summary))
    prompt += "\n\n\n\n"
    prompt += f"""
## Test Functions and Error Messages Summary
{processor.get_test_code_text()}

Here is a summary of the test cases and error messages:
{error_message_summary}""".strip()

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
