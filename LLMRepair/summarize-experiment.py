import json
from multiprocessing import process
import pickle
import threading
from pathlib import Path
from typing import Any, List

import tiktoken

from gpt_utils import get_responses_from_prompt, QueryException, get_and_save_response_with_fix_path
from utils import print_in_red, print_in_yellow, iter_bugid_folders, divide_list, print_in_green

total_usage = 0
n_partitions = 1  # number of threads
compression_cap = 0  # token size cap
database_folder_path = Path.cwd().parent / "training-data" / "summarize-experiment-v3"

LOG_MODE = n_partitions == 1


def log_red(message: str):
    if LOG_MODE:
        print_in_red(message)


def log_yellow(message: str):
    if LOG_MODE:
        log_yellow(message)


def log(*args, sep=' ', end='\n', file=None):
    if LOG_MODE:
        print(*args, sep=sep, end=end, file=file)


class Processor:
    def __init__(self, bug_folder: Path, bugid: str):
        self.bug_folder = bug_folder

        with open(bug_folder / "facts-in-prompt.json") as f:
            self.facts_in_prompt = json.load(f)

        with open(bug_folder / "bug-data.json") as f:
            json_data = json.load(f)
            __tmp0 = list(json_data[bugid].values())[0]
            self.function_source_code = __tmp0["buggy_functions"][0]["function_code"]
            self.file_path = list(json_data[bugid].keys())[0]

        with open(bug_folder / "facts.json") as f:
            self.fact_data = json.load(f)
        
        prompt_instruction_folder = Path.cwd() / "prompt_instructions"
        self._related_functions_instruction = (prompt_instruction_folder / "related_functions_v2.md").read_text()
        self._stacktrace_instruction = (prompt_instruction_folder / "stacktrace_v2.md").read_text()
        self._issue_description_instruction = (prompt_instruction_folder / "issue_description_v2.md").read_text()
        self._runtime_value_instruction = (prompt_instruction_folder / "runtime_value_v2.md").read_text()
        self._angelic_value_instruction = (prompt_instruction_folder / "angelic_value_v2.md").read_text()

        title = "## The error message from the failing test"
        error_messages = self.facts_in_prompt["5"].split(title)
        error_messages = [d.strip() for d in error_messages if d.strip() != ""]
        error_messages = [f"{title}\n{d}" for d in error_messages]
        
        title = "# A failing test function for the buggy function"
        test_cases = self.facts_in_prompt["4"].split(title)
        test_cases = [d.strip() for d in test_cases if d.strip() != ""]
        test_cases = [f"# Test case {i + 1} for the buggy function\n{d}" for i, d in enumerate(test_cases)]
        
        self.test_and_error_message = "\n\n\n".join([
            f"{a}\n\n{b}" for a, b in zip(test_cases, error_messages)
        ])

    @property
    def source_code_without_imports(self):
        prompt = "## The source code of the buggy function\n\n"
        prompt += "```python\n"
        prompt += self.function_source_code
        prompt += "\n```"
        return prompt

    @property
    def source_code_with_imports(self):
        prompt = "## The source code of the buggy function\n\n"
        if self.facts_in_prompt["1.3.3"] != "":
            prompt += self.facts_in_prompt["1.3.3"]
        prompt += f"The buggy function is under file: `{self.file_path}`\n\n\n"
        prompt += "```python\n"
        prompt += self.function_source_code
        prompt += "\n```\n\n\n"
        return prompt
    
    @property
    def related_functions_prompt(self):
        return self._related_functions_instruction.format(
            self.facts_in_prompt["source_code_body"],
        )
    
    @property
    def stack_trace_summary_prompt(self):
        return self._stacktrace_instruction.format(
            self.source_code_without_imports,
            self.test_and_error_message
        )

    @property
    def issue_description_prompt(self):
        return self._issue_description_instruction.format(
            self.source_code_without_imports,
            self.facts_in_prompt["8"].strip()
        )

    @property
    def runtime_value_prompt(self):
        return self._runtime_value_instruction.format(
            self.source_code_without_imports,
            self.facts_in_prompt["6"].strip()
        )

    @property
    def angelic_value_prompt(self):
        return self._angelic_value_instruction.format(
            self.source_code_without_imports,
            self.facts_in_prompt["7"].strip()
        )

def count_tokens(prompt: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(prompt))


def construct_prompt(processor: Processor) -> str:
    # initial instruction
    prompt = "Please fix the buggy function provided below and output a corrected version.\n\n\n"
    prompt += processor.facts_in_prompt["9"]
    prompt += "\n\n\n"

    # process buggy function and its imports
    prompt += processor.source_code_with_imports

    prompt += resolve_related_functions(processor)

    print(prompt)
    exit(0)

    prompt += resolve_stacktrace(processor)
    prompt += resolve_runtime_value(processor)
    prompt += resolve_angelic_value(processor)

    prompt += processor.facts_in_prompt["8"] # github issue is not affecting performance the most
    return prompt


def resolve_related_functions(processor: Processor):
    related_functions_prompt = processor.related_functions_prompt
    num_tokens = count_tokens(related_functions_prompt)
    if num_tokens > 16_000:
        log_red(f"Related functions summary is too long. Tokens: {num_tokens}")
        return ""
    
    if num_tokens < compression_cap:
        log("Preserving related functions. Tokens:", num_tokens)
        return related_functions_prompt
    
    log("Generating related functions summary. Tokens:", num_tokens, end=" ")
    related_functions_summary = get_response_and_store_results(prompt=related_functions_prompt,
                                                              prompt_file=processor.bug_folder / "related_functions_prompt.md",
                                                              response_file=processor.bug_folder / "related_functions_response.md",
                                                              pkl_file=processor.bug_folder / "related_functions_response.pkl")[0]
    log("->", count_tokens(related_functions_summary))

    result = "## Summary of Related Functions\n\n"
    result += related_functions_summary
    result += "\n\n\n"

    return result


def resolve_stacktrace(processor: Processor):
    if processor.facts_in_prompt["4"] == "" or processor.facts_in_prompt["5"] == "":
        log_red("No test info")
        return ""
    
    stacktrace_summary_prompt = processor.stack_trace_summary_prompt
    num_tokens = count_tokens(stacktrace_summary_prompt)
    if num_tokens > 16_000:
        log_red(f"Test info summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < compression_cap:
        log("Preserving test info. Tokens:", num_tokens)
        return processor.facts_in_prompt["5"]

    log("Generating test info. Tokens:", count_tokens(stacktrace_summary_prompt), end=" ")
    error_message_summary = get_response_and_store_results(prompt=stacktrace_summary_prompt,
                                                           prompt_file=processor.bug_folder / "test_info_prompt.md",
                                                           response_file=processor.bug_folder / "test_info_response.md",
                                                           pkl_file=processor.bug_folder / "test_info_response.pkl")[0]
    log("->", count_tokens(error_message_summary))

    result = "## Summary of the test cases and error messages\n\n"
    result += error_message_summary
    result += "\n\n\n"

    return result


def resolve_runtime_value(processor: Processor):
    if processor.facts_in_prompt["6"] == "":
        log_red("No runtime value")
        return ""
    
    runtime_value_prompt = processor.runtime_value_prompt
    num_tokens = count_tokens(runtime_value_prompt)
    if num_tokens > 16_000:
        log_red(f"Runtime value summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < compression_cap:
        log("Preserving runtime value. Tokens:", num_tokens)
        return processor.facts_in_prompt["6"]

    log("Generating runtime value summary. Tokens:", num_tokens, end=" ")
    runtime_value_summary = get_response_and_store_results(prompt=runtime_value_prompt,
                                                           prompt_file=processor.bug_folder / "runtime_info_prompt.md",
                                                           response_file=processor.bug_folder / "runtime_info_response.md",
                                                           pkl_file=processor.bug_folder / "runtime_info_response.pkl")[0]
    log("->", count_tokens(runtime_value_summary))

    result = "## Summary of Runtime Variables and Types in the Buggy Function\n\n"
    result += runtime_value_summary
    result += "\n\n\n"

    return result


def resolve_angelic_value(processor: Processor):
    if processor.facts_in_prompt["7"] == "":
        log_red("No angelic value")
        return ""
    
    angelic_value_prompt = processor.angelic_value_prompt
    num_tokens = count_tokens(angelic_value_prompt)
    if num_tokens > 16_000:
        log_red(f"Angelic value summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < compression_cap:
        log("Preserving angelic value. Tokens:", num_tokens)
        return processor.facts_in_prompt["7"]

    log("Generating angelic value summary. Tokens:", num_tokens, end=" ")
    angelic_value_summary = get_response_and_store_results(prompt=angelic_value_prompt,
                                                           prompt_file=processor.bug_folder / "angelic_info_prompt.md",
                                                           response_file=processor.bug_folder / "angelic_info_response.md",
                                                           pkl_file=processor.bug_folder / "angelic_info_response.pkl")[0]
    log("->", count_tokens(angelic_value_summary))

    result = "## Summary of Expected Parameters and Return Values in the Buggy Function\n\n"
    result += angelic_value_summary
    result += "\n\n\n"

    return result


def resolve_github_issue(processor: Processor):
    if processor.facts_in_prompt["8"] == "":
        log_red("No GitHub issue")
        return ""
    
    github_issue_prompt = processor.issue_description_prompt
    num_tokens = count_tokens(github_issue_prompt)
    if num_tokens > 16_000:
        log_red(f"GitHub issue summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < compression_cap:
        log("Preserving GitHub issue. Tokens:", num_tokens)
        return processor.facts_in_prompt["8"]

    log("Generating GitHub issue summary. Tokens:", num_tokens, end=" ")
    github_issue_summary = get_response_and_store_results(prompt=github_issue_prompt,
                                                          prompt_file=processor.bug_folder / "github_issue_prompt.md",
                                                          response_file=processor.bug_folder / "github_issue_response.md",
                                                          pkl_file=processor.bug_folder / "github_issue_response.pkl")[0]
    log("->", count_tokens(github_issue_summary))

    result = "## Summary of the GitHub Issue Related to the Bug\n\n"
    result += github_issue_summary
    result += "\n\n\n"

    return result


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


def process_each_bug(bugid: str, project_folder: Path, bugid_folder: Path):
    global total_usage
    global database_folder_path

    if bugid != "pandas:122":
        return

    print_in_green(f"Processing {bugid}...")
    facts_proc = Processor(bug_folder=bugid_folder, bugid=bugid)

    prompt = construct_prompt(facts_proc)
    with open(bugid_folder / "prompt.md", "w") as f:
        f.write(prompt)

    log("Generating patch response. Prompt tokens:", count_tokens(prompt))
    token_usage: Any = get_and_save_response_with_fix_path(prompt=prompt,
                                                           gpt_model="gpt-3.5-turbo-1106",
                                                           response_file_name_prefix="prompt_response",
                                                           database_dir=database_folder_path,
                                                           project_name=project_folder.name,
                                                           bug_id=bugid_folder.name,
                                                           trial=10)

    if type(token_usage) is dict:
        total_usage += token_usage["total_tokens"]
    else:
        total_usage += token_usage.total_tokens


def main():
    global database_folder_path
    global n_partitions

    partitions = divide_list(iter_bugid_folders(database_folder_path), n_partitions)

    def thread_func(folders):
        for bugid, project_folder, bugid_folder in folders:
            process_each_bug(bugid, project_folder, bugid_folder)

    threads = []  # List to keep track of the threads

    for partition in partitions:
        # create and start threads
        thread = threading.Thread(target=thread_func, args=(partition,))
        thread.start()
        threads.append(thread)  # Add the thread to the list of threads

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print_in_yellow(f"Total token usage: {total_usage}, estimate ${total_usage / 1000_000}")


if __name__ == "__main__":
    main()
