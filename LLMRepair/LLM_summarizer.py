import json
import textwrap
from collections import defaultdict

import tiktoken
import pickle
from pathlib import Path
from gpt_utils import get_responses_from_prompt, QueryException
from utils import print_in_red, print_in_yellow, iter_bugid_folders, get_function_code, get_facts_in_prompt, get_import_statements
from features_extractor import Facts
from typing import List, Tuple, Dict, Any


class CustomFactProcessor(Facts):

    def _post_init(self):
        self.buggy_function_code = ""
        self.test_function_code = defaultdict[str, List[str]](list)
        self.error_message = ""

        # begin processing
        with open(Path(self._bwd) / "bug-data.json") as f:
            json_data = json.load(f)
            self.load_from_json_object(json_data[self._bugid])

        self.facts_in_prompt = get_facts_in_prompt(Path(self._bwd))

    def get_test_function_prompt(self):
        # assign prompts
        prompts_sections = []
        for test_file_path, test_function_codes in self.test_function_code.items():
            section = ""
            section += f"The followings are test functions under directory `{test_file_path}` in the project.\n```python\n"
            section += "\n\n".join(test_function_codes)
            section += "\n```"
            prompts_sections.append(section)

        result = "\n\n".join(prompts_sections)
        result += f"\n\nThe error message that corresponds the the above test functions is:\n```\n{self.error_message}\n```"

        instruction = Path("prompt_instructions/test_info_summarize.txt").read_text()
        prompt = f"{instruction}\n\n"
        prompt += "The following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += result

        return prompt

    def get_dynamic_values_prompt(self):
        runtime_variables_section = self.facts_in_prompt["5"].split("# Expected variable value and type in tests")
        if len(runtime_variables_section) >= 1:
            runtime_variables_section = runtime_variables_section[1].strip()
        else:
            return ""
        instruction = Path("prompt_instructions/dynamic_value_summarize.txt").read_text()
        prompt = f"{instruction}\n\nThe following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += f"{runtime_variables_section}"
        return prompt

    def get_angelic_values_prompt(self):
        angelic_values_section = self.facts_in_prompt["5"].split("# Expected variable value and type in tests\n")
        if len(angelic_values_section) == 2:
            angelic_values_section = angelic_values_section[1].strip()
        else:
            return ""
        angelic_values_section = "# Expected return value in tests\n" + angelic_values_section
        instruction = Path("prompt_instructions/angelic_value_summarize.txt").read_text()
        prompt = f"{instruction}\n\nThe following is the buggy function code:\n"
        prompt += f"```python\n{self.buggy_function_code}\n```\n\n"
        prompt += f"{angelic_values_section}"
        return prompt

    def _resolve_buggy_function_code(self, buggy_function):
        self.buggy_function_code = buggy_function

    def _resolve_test_function_and_test_file_path(self, test_data):
        test_function_code = test_data["test_function_code"]
        test_file_path = self._remove_project_root(test_data["test_path"])
        self.test_function_code[test_file_path].append(textwrap.dedent(test_function_code))

    def _resolve_error_message_and_stacktrace(self, test_data):
        self.error_message = test_data["full_test_error"]


def get_response_and_store_results(prompt: str, prompt_file: Path, response_file: Path, pkl_file: Path, trials=1) -> List[str]:
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

    # prompt file
    draft_md_content = "# Prompt\n"
    draft_md_content += f"{prompt}\n\n"
    prompt_file.write_text(draft_md_content)

    # response file
    draft_md_content = "# Response\n"
    for i, response in enumerate(responses):
        draft_md_content += f"## Response {i + 1}\n{response}\n\n"
    response_file.write_text(draft_md_content)

    # pkl file
    with open(pkl_file, "wb") as dump_pickle_file:
        pickle.dump(responses, dump_pickle_file)

    return responses


general_prompt_template = """
Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.

Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
{0}
```

The following is the buggy function that you need to fix:
```python
{1}
```

{2}
""".strip()


def main():
    database_folder_path = Path.cwd().parent / "training-data" / "LLM_summarizer"

    for bugid, project_folder, bugid_folder in iter_bugid_folders(database_folder_path):
        if bugid != "black:19":
            continue
        print(f"Processing {bugid}...")

        facts_proc = CustomFactProcessor(bugid=bugid, bug_working_directory=bugid_folder)


        get_response_and_store_results(prompt=facts_proc.get_angelic_values_prompt(),
                                       prompt_file=bugid_folder / "angelic_info_prompt.md",
                                       response_file=bugid_folder / "angelic_info_response.md",
                                       pkl_file=bugid_folder / "angelic_info_response.pkl")


        # get_response_and_store_results(prompt=facts_proc.get_test_function_prompt(),
        #                                prompt_file=bugid_folder / "test_info_prompt.md",
        #                                response_file=bugid_folder / "test_info_response.md",
        #                                pkl_file=bugid_folder / "test_info_response.pkl")

        break


if __name__ == "__main__":
    main()
