import json
import pickle
import re
from pathlib import Path
from typing import List, Tuple

from gpt_utils import get_responses_from_prompt, QueryException
from utils import print_in_red

question_template = """
Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
{0}

Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."
"""

class_info_prompt_template = question_template.format(
    """
Assume you know the buggy function source code, does following used method signatures help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The class declaration containing the buggy function and used method signatures is:
```
{1}
```"""
)

file_info_prompt_template = question_template.format(
    """
Assume you know the buggy function source code, 
Does following used function signatures with the same file help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The used function signatures and file name are:
```
{1}
```"""
)

test_info_prompt_template = question_template.format(
    """Assume you know the buggy function source code, 
does following corresponding test code and error message for the buggy function helps to fix the bug?

The buggy function's source code is:
```python
{0}
```

The corresponding test code and error message are:
{1}"""
)

dynamic_info_prompt_template = question_template.format(
    """Assume you know the buggy function source code,
does following runtime variable values help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The runtime variable values are:
{1}"""
)

github_info_prompt_template = question_template.format(
    """Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
{0}
```

The github issue message is:
{1}"""
)


def is_response_positive(responses: List[str], bugid: str) -> bool:
    number_of_yes = 0
    yes_pattern = re.compile(r"Conclusion.*Yes", re.DOTALL)
    no_pattern = re.compile(r"Conclusion.*No", re.DOTALL)
    for response in responses:
        if yes_pattern.search(response):
            number_of_yes += 1
        elif not yes_pattern.search(response) and not no_pattern.search(response):
            print_in_red(f"Invalid response for {bugid}: {response}")
            raise QueryException("Invalid response")
    return number_of_yes >= 3


def get_bitvector_from_existing_responses(bugid_folder: Path, bugid: str):
    class_scope = bugid_folder / "response_Class_scope_based_facts.md"
    file_scope = bugid_folder / "response_File_scope_based_facts.md"
    test_scope = bugid_folder / "response_Test_info_based_facts.md"
    dynamic = bugid_folder / "response_Runtime_value_info_based_facts.md"
    github_scope = bugid_folder / "response_Github_issue_info_based_facts.md"

    paths = [class_scope, file_scope, test_scope, dynamic, github_scope]
    bitvector = ""
    for path in paths:
        if not path.exists():
            bitvector += "0"
        else:
            responses = path.read_text().strip().split("\n##")[1:]
            if is_response_positive(responses, bugid):
                bitvector += "1"
            else:
                bitvector += "0"

    return bitvector


def get_result_bitvector(_prompts: List[str], _bug_folder: Path, bugid: str) -> str:
    prompt_title = [
        "Class scope based facts",
        "File scope based facts",
        "Test info based facts",
        "Runtime value info based facts",
        "Github issue info based facts",
    ]
    prompt_file_title = [s.replace(" ", "_") for s in prompt_title]

    _bitvector = ""
    for idx, prompt in enumerate(_prompts):
        if prompt == "":
            _bitvector += "0"
            continue

        # save prompt
        prompt_file = _bug_folder / f"prompt_{prompt_file_title[idx]}.md"
        response_file = _bug_folder / f"response_{prompt_file_title[idx]}.md"
        if prompt_file.exists() and response_file.exists():
            print(f"result for {prompt_file_title[idx]} already exists")
            continue
        prompt_file_content = f"# Prompt {prompt_title[idx]}\n{prompt}\n\n"
        prompt_file.write_text(prompt_file_content)

        try:
            print(f"Querying for {prompt_file_title[idx]}")
            raw_responses = get_responses_from_prompt(
                prompt=prompt, model="gpt-3.5-turbo-1106", trial=5, temperature=1
            )

            # save raw response for the sake of money
            dump_pickle_file = _bug_folder / f"response_{prompt_file_title[idx]}.pkl"
            with open(dump_pickle_file, "wb") as dump_pickle_file:
                pickle.dump(raw_responses, dump_pickle_file)

            responses = raw_responses["responses"]

            # save result
            draft_md_content = f"# Responses\n"
            for i, response in enumerate(responses):
                draft_md_content += f"## Response {i + 1}\n{response}\n\n"
            response_file.write_text(draft_md_content)

            # determine result

            if is_response_positive(responses, bugid) >= 3:
                _bitvector += "1"
            else:
                _bitvector += "0"

        except QueryException as error:
            print_in_red(f"{error}")

    return _bitvector


def main():
    bug_folder = (
        Path.cwd().parent / "training-data" / "16-16-dataset-llm-feature-selector"
    )
    bugs: List[Tuple[Path, str]] = []
    for project_folder in bug_folder.iterdir():
        if not project_folder.is_dir():
            continue
        for bug_folder in project_folder.iterdir():
            if not bug_folder.is_dir():
                continue
            bugs.append((bug_folder, f"{project_folder.name}:{bug_folder.name}"))

    for bug_folder, bugid in bugs:
        facts_in_prompt_file = bug_folder / "facts-in-prompt.json"
        facts = list(json.loads(facts_in_prompt_file.read_text()).values())[1:6]

        bug_data_file = bug_folder / "bug-data.json"
        __tmp0 = list(json.loads(bug_data_file.read_text())[bugid].values())[0]
        source_code = __tmp0["buggy_functions"][0]["function_code"]

        prompts = [
            class_info_prompt_template.format(source_code, facts[0])
            if facts[0]
            else "",
            file_info_prompt_template.format(source_code, facts[1]) if facts[1] else "",
            test_info_prompt_template.format(source_code, facts[2]) if facts[2] else "",
            dynamic_info_prompt_template.format(source_code, facts[3])
            if facts[3]
            else "",
            github_info_prompt_template.format(source_code, facts[4])
            if facts[4]
            else "",
        ]

        try:
            print(f"Generating bitvector for {bugid}")
            bitvector = get_result_bitvector(prompts, bug_folder, bugid)

        except QueryException as error:
            print_in_red(f"{error}")
            continue

        bitvector_file = bug_folder / "bitvector.txt"
        bitvector_file.write_text(bitvector)
