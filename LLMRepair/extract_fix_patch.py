import json
import os
import re
from typing import Optional

from utils import extract_function_from_response, print_in_red, print_in_yellow


def find_patch_from_response(raw_response: str, buggy_function_name: str) -> Optional[str]:
    code_block_pattern = r"```(?:python\n)?(.*?)(?:\n)?```"
    function_pattern = rf".*def.*{buggy_function_name}.*"

    code_blocks = re.findall(code_block_pattern, raw_response, re.DOTALL)
    for code_block in code_blocks:
        if re.search(function_pattern, code_block, re.DOTALL):
            return code_block
    return None


stratum_path = "/Users/jerry/Documents/GitHub/LLM-prompt-data-for-APR/preliminary-study/second-stratum"

for project_name in os.listdir(stratum_path):
    if not os.path.isdir(os.path.join(stratum_path, project_name)):
        continue
    for bug_id in os.listdir(os.path.join(stratum_path, project_name)):
        bug_dir = os.path.join(stratum_path, project_name, bug_id)
        if not os.path.isdir(bug_dir):
            continue

        if project_name == "pandas" and bug_id == "124":
            continue

        bug_path = os.path.join(stratum_path, bug_dir)
        responses_files = [
            path
            for path in os.listdir(bug_path)
            if ("response" in path) and ("md" in path)
        ]

        bug_data_file = os.path.join(bug_path, "bug-data.json")

        if not os.path.exists(bug_data_file):
            continue

        with open(os.path.join(bug_path, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = json.load(bug_data_file)[project_name + ":" + bug_id]
            user_dir: str = list(bug_data)[0]
            buggy_function_code: str = bug_data[user_dir]["buggy_functions"][0]["function_code"]
            buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
            buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]

        for response_file_name in responses_files:
            with open(os.path.join(bug_path, response_file_name), "r") as response_file:
                response = response_file.read()
                fix_patch = find_patch_from_response(response, buggy_function_name)

            if fix_patch is not None:
                try:
                    fix_patch = extract_function_from_response(fix_patch, buggy_function_name)

                    if fix_patch is None:
                        print_in_red(
                            f"{bug_dir}/{response_file_name} doesn't contain valid fix patch, default treat it as incorrect"
                        )
                        fix_patch = ""

                except SyntaxError:
                    print_in_red(
                        f"{bug_dir}/{response_file_name} doesn't contain valid fix patch, default treat it as incorrect"
                    )
                    fix_patch = ""

            else:
                print_in_yellow(
                    f"{bug_dir}/{response_file_name} doesn't have a response, default treat it as incorrect"
                )

            used_facts = [int(char) for char in response_file_name[:17]]
            bitvector = {
                "1.3.1": used_facts[0],
                "1.3.2": used_facts[1],
                "1.2.1": used_facts[2],
                "1.2.2": used_facts[3],
                "1.2.3": used_facts[4],
                "1.1.2": used_facts[5],
                "2.1.3": used_facts[6],
                "2.1.4": used_facts[7],
                "2.1.5": used_facts[8],
                "2.1.6": used_facts[9],
                "1.4.1": used_facts[10],
                "1.4.2": used_facts[11],
                "2.1.1": used_facts[12],
                "2.1.2": used_facts[13],
                "3.1.1": used_facts[14],
                "3.1.2": used_facts[15],
                "cot": used_facts[16],
            }

            prefix = project_name + "/"
            start_idx = user_dir.find(prefix) + len(prefix)
            buggy_location_file_name = user_dir[start_idx:]

            test_input_data = {
                project_name: [
                    {
                        "bugID": int(bug_id),
                        "bitvector": bitvector,
                        "start_line": buggy_function_start_line,
                        "file_name": buggy_location_file_name,
                        "replace_code": fix_patch,
                    }
                ]
            }

            test_input_path = os.path.join(
                bug_path, response_file_name[: response_file_name.find("m")] + "json"
            )

            with open(test_input_path, "w") as test_input_file:
                json.dump(test_input_data, test_input_file, indent=4)
