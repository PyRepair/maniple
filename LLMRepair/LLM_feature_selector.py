import argparse
import json
from pathlib import Path
from typing import List, Tuple

from utils import print_in_red, print_in_yellow
from gpt_utils import get_responses_from_prompt, QueryException


question_template = """
Your task is to determine if the provided fact is useful and relevant in correcting the buggy function's source code.
{0}

Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."
"""

class_info_prompt_template = question_template.format("""
Does following class information containing buggy function help to fix the bug?

```python
{0}
```""")

print(class_info_prompt_template)

bug_folder = Path.cwd().parent / "training-data" / "16-16-dataset-llm-feature-selector"
print(bug_folder)

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
    facts = list(json.loads(facts_in_prompt_file.read_text()).values())[1:]

    bug_data_file = bug_folder / "bug-data.json"
    __tmp0 = list(json.loads(bug_data_file.read_text())[bugid].values())[0]
    source_code = __tmp0["buggy_functions"][0]["function_code"]

    print(len(facts))

    # try:
    #     responses = get_responses_from_prompt(
    #         prompt=question, model="gpt-3.5-turbo-1106", trial=6
    #     )["responses"]
    #     print(responses)

    # except QueryException as error:
    #     print_in_red(f"{error}")
