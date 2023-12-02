import json
import os
import re
from utils import extract_function_from_response


def get_code_blocks(raw_response: str) -> list[str]:
    code_block_pattern = r'```(?:python\n)?(.*?)(?:\n)?```'
    return re.findall(code_block_pattern, raw_response, re.DOTALL)


stratum_path = "../preliminary-study/first-stratum"
first_stratum_path = os.listdir(stratum_path)

for bug_dir in first_stratum_path:
    project_name = bug_dir.rsplit('-', 1)[0]
    bug_id = bug_dir.rsplit('-', 1)[1]

    bug_path = os.path.join(stratum_path, bug_dir)
    responses_files = [path for path in os.listdir(bug_path) if ("response" in path) and ("md" in path)]

    with open(os.path.join(bug_path, "bug-data.json"), "r") as bug_data_file:
        bug_data: dict = json.load(bug_data_file)[project_name + ":" + bug_id]
        user_dir: str = list(bug_data)[0]
        buggy_function_code: str = bug_data[user_dir]["buggy_functions"][0]["function_code"]
        buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
        buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]

    for response_file_name in responses_files:
        with open(os.path.join(bug_path, response_file_name), "r") as response_file:
            response = response_file.read()
            code_blocks = get_code_blocks(response)

        fix_patch = ""
        if len(code_blocks) > 1:
            buggy_function_signature = ""
            for statement in buggy_function_code.split('\n'):
                buggy_function_signature += statement
                if ("def " + buggy_function_name) in statement:
                    break
                else:
                    buggy_function_signature += "\n"

            for code_block in code_blocks:
                if buggy_function_signature in code_block:
                    fix_patch = code_block
                    break

        elif len(code_blocks) == 0:
            fix_patch = ""

        else:
            fix_patch = code_blocks[0]

        if fix_patch != "":
            try:
                fix_patch = extract_function_from_response(fix_patch, buggy_function_name)

                if fix_patch is None:
                    fix_patch = ""

            except SyntaxError:
                print(
                    f"{bug_dir}/{response_file_name} doesn't contain valid fix patch, default treat it as incorrect")
                fix_patch = ""

        used_facts = [int(char) for char in response_file_name[:11]]
        print(response_file_name)
        bitvector = {
            "1.3.2": used_facts[0],
            "1.2.4": used_facts[1],
            "1.2.1": used_facts[2],
            "1.3.4": used_facts[3],
            "2.1.1": used_facts[4],
            "2.1.2": used_facts[5],
            "2.2.1": used_facts[6],
            "2.2.2": used_facts[7],
            "3.1.1": used_facts[8],
            "3.1.2": used_facts[9],
            "cot": used_facts[10]
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
                    "replace_code": fix_patch
                }
            ]
        }

        test_input_path = os.path.join(bug_path, response_file_name[:response_file_name.find("m")] + "json")
        with open(test_input_path, "w") as test_input_file:
            json.dump(test_input_data, test_input_file, indent=4)
