import json
import pickle
from re import S
import threading
from pathlib import Path
from typing import Any, List, Callable
import os

import tiktoken

from maniple.utils.openai_utils import (
    get_responses_from_prompt,
    QueryException,
    get_and_save_response_with_fix_path,
)
from maniple.utils.misc import (
    print_in_red,
    print_in_yellow,
    iter_bugid_folders,
    divide_list,
    print_in_green,
)
from maniple.utils.patch_validator import validate_patches
from maniple.utils.init_data import init_data
from maniple.metrics.check_pass_k import analyze as check_pass_k, pass_at_k
from maniple.maniple import clear_responses, clear_results


class Processor:
    def __init__(self, bug_folder: Path, bugid: str):
        self.bug_folder = bug_folder

        with open(bug_folder / "facts-in-prompt.json") as f:
            self.facts_in_prompt = json.load(f)

        with open(bug_folder / "static-dynamic-facts.json") as f:
            json_data = json.load(f)
            __tmp0 = list(json_data[bugid].values())[0]
            self.function_source_code = __tmp0["buggy_functions"][0]["function_code"]
            self.file_path = self._remove_project_root(
                bugid, list(json_data[bugid].keys())[0]
            )

        with open(bug_folder / "processed-facts.json") as f:
            self.fact_data = json.load(f)

        title = "### The error message from the failing test"
        error_messages = self.facts_in_prompt["5"].split(title)
        error_messages = [d.strip() for d in error_messages if d.strip() != ""]
        error_messages = [f"{title}\n{d}" for d in error_messages]

        title = "## A failing test function for the buggy function"
        test_cases = self.facts_in_prompt["4"].split(title)
        test_cases = [d.strip() for d in test_cases if d.strip() != ""]
        test_cases = [
            f"## Test case {i + 1} for the buggy function\n{d}"
            for i, d in enumerate(test_cases)
        ]

        self.test_and_error_message = "\n\n\n".join(
            [f"{a}\n\n{b}" for a, b in zip(test_cases, error_messages)]
        )

    @staticmethod
    def _remove_project_root(bugid: str, path: str):
        bugid_label = bugid.replace(":", "_")
        idx = path.find(bugid_label)

        if idx == -1:
            project_name = bugid.split(":")[0]
            idx = path.find(project_name)
            if idx == -1:
                return path
            return path[idx + len(project_name) + 1 :]

        return path[idx + len(bugid_label) + 1 :]

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


class Dataset:
    def __init__(
        self, dataset: str, output_path=None, envs_dir=None, init_data_folder=None
    ) -> None:
        self.database_path = dataset if output_path is None else output_path

        # If not initialized, create the database
        if not os.path.exists(self.database_path):
            init_data(self.database_path, dataset, init_data_folder)

        self.envs_dir = envs_dir

        self.log_mode = False

        self._total_usage = 0

    def log_red(self, message: str):
        if self.log_mode:
            print_in_red(message)


    def log_yellow(self, message: str):
        if self.log_mode:
            print_in_yellow(message)


    def log(self, *args, sep=" ", end="\n", file=None):
        if self.log_mode:
            print(*args, sep=sep, end=end, file=file)

    def for_each_bug(
        self,
        task_name="prompt",
        fn: Callable[[Processor], str] | None = None,
        n_partitions=1,
        bugids=None,
        gen_patch=False,
        trials=1,
        model="gpt-3.5-turbo-1106",
    ):
        origin_log_mode = self.log_mode
        if n_partitions == 1:
            self.log_mode = False

        if bugids is None:
            bugids = []  # list of bugids to restrict

        partitions = divide_list(
            iter_bugid_folders(Path(self.database_path)), n_partitions
        )

        def thread_func(folders):
            for bugid, project_folder, bugid_folder in folders:
                if bugids and bugid not in bugids:
                    continue

                print_in_green(f"Processing {bugid}...")
                facts_proc = Processor(bug_folder=bugid_folder, bugid=bugid)

                if fn is None:
                    prompt = (bugid_folder / "prompt.md").read_text()
                else:
                    prompt = fn(facts_proc)
                    with open(bugid_folder / "prompt.md", "w") as f:
                        f.write(prompt)

                if gen_patch:
                    self.log(
                        "Generating patch response. Prompt tokens:",
                        count_tokens(prompt),
                    )
                    token_usage: Any = get_and_save_response_with_fix_path(
                        prompt=prompt,
                        gpt_model=model,
                        actual_group_bitvector=task_name,
                        database_dir=self.database_path,
                        project_name=project_folder.name,
                        bug_id=bugid_folder.name,
                        trial=trials,
                    )

                    if type(token_usage) is dict:
                        self._total_usage += token_usage["total_tokens"]
                    else:
                        self._total_usage += token_usage.total_tokens

        threads = []  # List to keep track of the threads

        for partition in partitions:
            # create and start threads
            thread = threading.Thread(target=thread_func, args=(partition,))
            thread.start()
            threads.append(thread)  # Add the thread to the list of threads

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print_in_yellow(
            f"Total token usage: {self._total_usage}, estimate ${self._total_usage / 1000_000}"
        )

        self.log_mode = origin_log_mode

    def get_response_and_store_results(
        self, prompt: str, prompt_file: Path, response_file: Path, pkl_file: Path, trials=1
    ) -> List[str]:
        # if this prompt is too long just set bit to 0
        # we need to estimate tokens first
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(prompt))
        if num_tokens > 16000:
            raise QueryException(f"Prompt is exceeding 16000 tokens")

        gpt_response = get_responses_from_prompt(
            prompt=prompt, model="gpt-3.5-turbo-1106", trial=trials, temperature=1
        )
        responses: List[str] = gpt_response["responses"]
        self._total_usage += gpt_response["total_token_usage"].total_tokens

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

    def validate_each_bug(self, bugids=None):
        if bugids is None:
            bugids = [s for s, _, _ in iter_bugid_folders(Path(self.database_path))]

        for bugid in bugids:
            bwd = os.path.join(self.database_path, *bugid.split(":"))
            validate_patches(
                bugid, bwd, envs_dir=self.envs_dir, use_docker=False, overwrite=True
            )

    def show_pass_k(self):
        _, _, total_fixes_per_bug, total_trials_per_bug = check_pass_k(
            [Path(self.database_path)]
        )

        pass_k_sum = [0.0] * 10

        for _bugid in total_trials_per_bug.keys():
            fixes_count = total_fixes_per_bug[_bugid]
            trials_count = total_trials_per_bug[_bugid]

            print(f"Bug {_bugid} current: {fixes_count}/{total_trials_per_bug[_bugid]}")

            for k in range(1, 11):
                pass_k_sum[k - 1] += pass_at_k(trials_count, fixes_count, k)

        for k in range(1, 11):
            print(
                f"pass@{k} current: {pass_k_sum[k - 1] / len(total_fixes_per_bug.keys())}"
            )

    def clear(self):
        clear_responses(self.database_path)
        clear_results(self.database_path)
