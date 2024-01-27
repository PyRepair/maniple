import json
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

class_info_prompt_template = question_template.format("""
Assume you know the buggy function source code, does following used method signatures help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The class declaration containing the buggy function and used method signatures is:
```
{1}
```""")

file_info_prompt_template = question_template.format("""
Assume you know the buggy function source code, 
Does following used function signatures with the same file help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The used function signatures and file name are:
```
{1}
```""")

test_info_prompt_template = question_template.format("""Assume you know the buggy function source code, 
does following corresponding test code and error message for the buggy function helps to fix the bug?

The buggy function's source code is:
```python
{0}
```

The corresponding test code and error message are:
{1}""")

dynamic_info_prompt_template = question_template.format("""Assume you know the buggy function source code,
does following runtime variable values help to fix the bug?

The buggy function's source code is:
```python
{0}
```

The runtime variable values are:
{1}""")

github_info_prompt_template = question_template.format("""Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
{0}
```

The github issue message is:
{1}""")

bug_folder = Path.cwd().parent / "training-data" / "16-16-dataset-llm-feature-selector"
bugs: List[Tuple[Path, str]] = []
for project_folder in bug_folder.iterdir():
    if not project_folder.is_dir():
        continue
    for bug_folder in project_folder.iterdir():
        if not bug_folder.is_dir():
            continue
        bugs.append((bug_folder, f"{project_folder.name}:{bug_folder.name}"))

test_bugs = [
    [Path.cwd().parent / "training-data" / "16-16-dataset-llm-feature-selector" / "pandas" / "48", "pandas:48"]
]

for bug_folder, bugid in test_bugs:
    facts_in_prompt_file = bug_folder / "facts-in-prompt.json"
    facts = list(json.loads(facts_in_prompt_file.read_text()).values())[1:6]

    bug_data_file = bug_folder / "bug-data.json"
    __tmp0 = list(json.loads(bug_data_file.read_text())[bugid].values())[0]
    source_code = __tmp0["buggy_functions"][0]["function_code"]

    prompts = [
        class_info_prompt_template.format(source_code, facts[0]) if facts[0] else "",
        file_info_prompt_template.format(source_code, facts[1]) if facts[1] else "",
        test_info_prompt_template.format(source_code, facts[2]) if facts[2] else "",
        dynamic_info_prompt_template.format(source_code, facts[3]) if facts[3] else "",
        github_info_prompt_template.format(source_code, facts[4]) if facts[4] else "",
    ]

    prompts_file = bug_folder / "prompts.md"
    prompts_file.write_text(f"""# Prompts
## Class scope based facts
{prompts[0]}
## File scope based facts
{prompts[1]}
## Test info based facts
{prompts[2]}
## Runtime value info based facts
{prompts[3]}
## Github issue info based facts
{prompts[4]}""")

    bitvector = ""

    for idx, prompt in enumerate(prompts):
        if prompt == "":
            bitvector += "0"
            continue

        try:
            responses = get_responses_from_prompt(
                prompt=prompt,
                model="gpt-3.5-turbo-1106",
                trial=5,
                temperature=1
            )["responses"]

            # save result
            response_file = bug_folder / f"response{idx + 1}.md"
            draft_md_content = "# Responses\n"
            for _idx0, response in enumerate(responses):
                draft_md_content += f"## Response {_idx0 + 1}\n"
                draft_md_content += f"{response}\n\n"
            response_file.write_text(draft_md_content)

            # determine result
            number_of_yes = 0
            yes_pattern = re.compile(r'Conclusion.*Yes')
            no_pattern = re.compile(r'Conclusion.*No')
            for response in responses:
                if yes_pattern.search(response):
                    number_of_yes += 1
                elif not yes_pattern.search(response) and not no_pattern.search(response):
                    print_in_red(f"Invalid response for {bugid}: {response}")
                    continue

            if number_of_yes >= 3:
                bitvector += "1"
            else:
                bitvector += "0"

        except QueryException as error:
            print_in_red(f"{error}")

    bitvector_file = bug_folder / "bitvector.txt"
    bitvector_file.write_text(bitvector)
