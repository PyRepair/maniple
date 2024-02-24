import json
import pickle
import threading
from pathlib import Path
from typing import Any, List, Callable

import tiktoken

from maniple.utils.openai_utils import get_responses_from_prompt, QueryException, get_and_save_response_with_fix_path
from maniple.utils.misc import print_in_red, print_in_yellow, iter_bugid_folders, divide_list, print_in_green

TOTAL_USAGE = 0
LOG_MODE = False
COMPRESSION_CAP = 0


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
            self.file_path = self._remove_project_root(bugid, list(json_data[bugid].keys())[0])

        with open(bug_folder / "facts.json") as f:
            self.fact_data = json.load(f)

        prompt_instruction_folder = Path(__file__).parent / "prompt_instructions"
        self._related_functions_instruction = (prompt_instruction_folder / "related_functions.md").read_text()
        self._stacktrace_instruction = (prompt_instruction_folder / "stacktrace_v2.md").read_text()
        self._issue_description_instruction = (prompt_instruction_folder / "issue_description_v2.md").read_text()
        self._runtime_value_instruction = (prompt_instruction_folder / "runtime_value_v2.md").read_text()
        self._angelic_value_instruction = (prompt_instruction_folder / "angelic_value_v2.md").read_text()

        title = "### The error message from the failing test"
        error_messages = self.facts_in_prompt["5"].split(title)
        error_messages = [d.strip() for d in error_messages if d.strip() != ""]
        error_messages = [f"{title}\n{d}" for d in error_messages]

        title = "## A failing test function for the buggy function"
        test_cases = self.facts_in_prompt["4"].split(title)
        test_cases = [d.strip() for d in test_cases if d.strip() != ""]
        test_cases = [f"## Test case {i + 1} for the buggy function\n{d}" for i, d in enumerate(test_cases)]

        self.test_and_error_message = "\n\n\n".join([
            f"{a}\n\n{b}" for a, b in zip(test_cases, error_messages)
        ])

    @staticmethod
    def _remove_project_root(bugid: str, path: str):
        bugid_label = bugid.replace(":", "_")
        idx = path.find(bugid_label)

        if idx == -1:
            project_name = bugid.split(":")[0]
            idx = path.find(project_name)
            if idx == -1:
                return path
            return path[idx + len(project_name) + 1:]

        return path[idx + len(bugid_label) + 1:]

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
        prompt += f"The buggy function is under file: `{self.file_path}`\n\nHere is the buggy function:\n"
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


def get_prompt_with_test_summary(processor: Processor, test_summary: str) -> str:
    return f"""
Please fix the buggy function provided below and output a corrected version.
{processor.facts_in_prompt["9"].strip()}


{processor.facts_in_prompt["1.3.3"].strip()}

## The source code of the buggy function
```python
# The relative path of the buggy file: {processor.file_path}

{processor.facts_in_prompt['source_code_body']}```

{test_summary}

{processor.facts_in_prompt["6"]}

{processor.facts_in_prompt["7"]}

{processor.facts_in_prompt["8"]}
    """.strip()


def count_tokens(prompt: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(prompt))


def resolve_related_functions(processor: Processor):
    if processor.facts_in_prompt["2"] == "" and processor.facts_in_prompt["3"] == "":
        log_red("No used function info")
        return ""

    related_functions_prompt = processor.related_functions_prompt
    num_tokens = count_tokens(related_functions_prompt)
    if num_tokens > 16_000:
        log_red(f"Related functions summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
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


def summarize_test_info(processor: Processor):
    if processor.facts_in_prompt["4"] == "" or processor.facts_in_prompt["5"] == "":
        log_red("No test info")
        return ""

    stacktrace_summary_prompt = processor.stack_trace_summary_prompt
    num_tokens = count_tokens(stacktrace_summary_prompt)
    if num_tokens > 16_000:
        log_red(f"Test info summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
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

    if num_tokens < COMPRESSION_CAP:
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

    if num_tokens < COMPRESSION_CAP:
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

    if num_tokens < COMPRESSION_CAP:
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
    global TOTAL_USAGE

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
    TOTAL_USAGE += gpt_response["total_token_usage"].total_tokens

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


def for_each_bug(database_folder_path: Path, fn: Callable[[Processor], str], n_partitions=1, compression_cap=0, restricted_bugs=None, gen_patch=False):
    global TOTAL_USAGE
    TOTAL_USAGE = 0

    global LOG_MODE
    LOG_MODE = n_partitions == 1

    global COMPRESSION_CAP
    COMPRESSION_CAP = compression_cap

    if restricted_bugs is None:
        restricted_bugs = []  # list of bugids to restrict

    partitions = divide_list(iter_bugid_folders(database_folder_path), n_partitions)

    def thread_func(folders):
        global TOTAL_USAGE

        for bugid, project_folder, bugid_folder in folders:
            if restricted_bugs and bugid not in restricted_bugs:
                continue

            print_in_green(f"Processing {bugid}...")
            facts_proc = Processor(bug_folder=bugid_folder, bugid=bugid)

            prompt = fn(facts_proc)

            with open(bugid_folder / "prompt.md", "w") as f:
                f.write(prompt)

            if gen_patch:
                log("Generating patch response. Prompt tokens:", count_tokens(prompt))
                token_usage: Any = get_and_save_response_with_fix_path(prompt=prompt,
                                                                       gpt_model="gpt-3.5-turbo-1106",
                                                                       response_file_name_prefix="prompt_response",
                                                                       database_dir=database_folder_path,
                                                                       project_name=project_folder.name,
                                                                       bug_id=bugid_folder.name,
                                                                       trial=10)

                if type(token_usage) is dict:
                    TOTAL_USAGE += token_usage["total_tokens"]
                else:
                    TOTAL_USAGE += token_usage.total_tokens

    threads = []  # List to keep track of the threads

    for partition in partitions:
        # create and start threads
        thread = threading.Thread(target=thread_func, args=(partition,))
        thread.start()
        threads.append(thread)  # Add the thread to the list of threads

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print_in_yellow(f"Total token usage: {TOTAL_USAGE}, estimate ${TOTAL_USAGE / 1000_000}")
