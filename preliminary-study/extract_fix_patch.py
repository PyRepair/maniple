import json
import os
import re


def get_code_blocks(raw_response: str) -> list[str]:
    code_block_pattern = r'```(?:python\n)?(.*?)(?:\n)?```'
    return re.findall(code_block_pattern, raw_response, re.DOTALL)


def revise_fix_patch(patch: str):
    pass


first_stratum_path = os.listdir("first-stratum")

for bug_dir in first_stratum_path:
    project_name = bug_dir.rsplit('-', 1)[0]
    bug_id = bug_dir.rsplit('-', 1)[1]

    bug_path = os.path.join("first-stratum", bug_dir)
    responses_dir = [path for path in os.listdir(bug_path) if "response" in path]

    for response_dir in responses_dir:
        with open(os.path.join(bug_path, response_dir), "r") as response_file:
            response = response_file.read()
            code_blocks = get_code_blocks(response)

        fix_patch = ""
        if len(code_blocks) > 1:
            bug_data_path = os.path.join(bug_path, "bug-data.json")
            with open(bug_data_path, "r") as bug_data_file:
                bug_data: dict = json.load(bug_data_file)[project_name + ":" + bug_id]
                buggy_function_code: str = bug_data[list(bug_data)[0]]["buggy_functions"][0]["function_code"]

                buggy_function_signature = ""
                for statement in buggy_function_code.split('\n'):
                    buggy_function_signature += statement

                    if "def" not in statement:
                        buggy_function_signature += "\n"
                    else:
                        break

            for code_block in code_blocks:
                if buggy_function_signature in code_block:
                    fix_patch = code_block
                    break

        else:
            fix_patch = code_blocks[0]

        if fix_patch != "":
            revise_fix_patch(fix_patch)
            correct = 0
        else:
            correct = 0
