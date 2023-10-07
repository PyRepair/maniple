from os import path, makedirs
from typing import Dict, List
import argparse
import re

import openai
import sys
import json

sys.path.append('..')

openai.api_key = "rg-B09kO5jDDdG0axfeuA5YP0LLTX8Fxi0rxNrgtzU6ZfiPRVNE"
openai.api_base = "https://ai.redgatefoundry.com/v1"

database = ""
project = ""
prompt_type = 1
feature_split = 1
model = ""
repeat = 1


def main():
    parser = argparse.ArgumentParser(description="Create prompt and write result")
    parser.add_argument('-d', '--database', help="Database name, should be a folder under the database directory",
                        type=str, required=True)
    parser.add_argument('-p', '--project', help="Project name", type=str, required=True)
    parser.add_argument('-t', '--type', help="Prompt type, single: 0, multi: 1", required=True, type=int)
    parser.add_argument('-f', '--feature_split',
                        help="Split features, and drop one feature every run. 0: all feature, 1: split", required=True,
                        type=int)
    parser.add_argument('-m', '--model', help="LLM model name, Should be 'gpt-4' or 'gpt-3.5-turbo'",
                        required=True, type=str)
    parser.add_argument('-r', '--repeat', help="how many times answer are generated for a prompt",
                        required=True, type=int)

    args = parser.parse_args()

    global database, project, prompt_type, feature_split, model, repeat

    database = args.database
    project = args.project
    prompt_type = args.type
    feature_split = args.feature_split
    model = args.model
    repeat = args.repeat

    # load project data form database
    project_name = args.project
    data_address = path.join("..", "database", args.database, "bugs-data", project_name + ".json")
    bugs_data = json.load(open(data_address, "r", encoding="utf-8"))

    # traversal whole dataset, generate prompt and answer for every bug
    if args.type == 0:
        write_directory = path.join("..", "prompt-results", "single-prompt", args.database, args.model, args.project)
    else:
        write_directory = path.join("..", "prompt-results", "multi-prompt", args.database, args.model, args.project)
    traversal_bugs(bugs_data, args.feature_split, write_directory, args.repeat, args.model)


def traversal_bugs(bugs_data, feature_split: int, write_directory: str, number_of_answers: int, llm_model: str):
    for bug_index in range(len(bugs_data["bugs"])):
        bug_id = bugs_data["bugs"][bug_index]["id"]

        # only use available features
        exist_features = []
        exist_feature_indexes = []

        feature_index = 0
        for feature in bugs_data["bugs"][bug_index]["features"]:
            if bugs_data["bugs"][bug_index]["features"][feature] is not None:
                exist_features.append(feature)
                exist_feature_indexes.append(feature_index)
                feature_index += 1

        # run with all features
        if feature_split == 0:
            generate_single_prompt_answers(bugs_data["bugs"][bug_index], exist_features, exist_feature_indexes,
                                           write_directory, bug_id, number_of_answers, llm_model)
        elif feature_split == 1:
            # drop only one feature once
            for drop_index in range(len(exist_features)):
                selected_features = exist_features.copy()
                selected_features.pop(drop_index)
                selected_indexes = exist_feature_indexes.copy()
                selected_indexes.pop(drop_index)

                generate_single_prompt_answers(bugs_data["bugs"][bug_index], selected_features, selected_indexes,
                                               write_directory, bug_id, number_of_answers, llm_model)


def extract_code_snippets(answer: str):
    code_snippets = []
    code_block_pattern = r'```(?:python)?(.*?)```'
    code_blocks = re.findall(code_block_pattern, answer, re.DOTALL)

    for code_block in code_blocks:
        code_snippets.append(code_block.strip())

    return "\n".join(code_snippets)


def remove_import_statement(code_snippet: str) -> str:
    # Define a regular expression pattern to match import statements
    import_pattern = r'^\s*import\s+.*?$|^\s*from\s+\S+\s+import\s+.*?$'

    # Use re.sub to replace all matching import statements with an empty string
    cleaned_code = re.sub(import_pattern, '', code_snippet, flags=re.MULTILINE)

    # Remove any leading and trailing whitespace
    cleaned_code = cleaned_code.strip()

    return cleaned_code


def generate_single_prompt_answers(bug_info, selected_features: List[str], selected_indexes: List[int],
                                   write_directory: str, bug_id: int, number_of_answers: int, llm_model: str):
    prompt_filename = "prompt"
    for selected_index in selected_indexes:
        prompt_filename += "-"
        prompt_filename += str(selected_index)

    prompt_filename += ".md"

    # Build prompt from template
    prompt = build_prompt(bug_info, selected_features)

    # write prompt into md file
    write_prompt(prompt, write_directory, bug_id, prompt_filename)

    # repeat to get answer, number are defined by user input
    for number in range(number_of_answers):
        answer_filename = "answer"
        for selected_index in selected_indexes:
            answer_filename += "-"
            answer_filename += str(selected_index)

        answer_filename = answer_filename + "(" + str(number + 1) + ")"

        # connect to chatgpt to get answer
        answer = get_answer_from_chatgpt(prompt, llm_model)

        code_snippet = extract_code_snippets(answer)

        function_snippet = remove_import_statement(code_snippet)

        # write answer into md file
        write_answer_markdown(answer, write_directory, bug_id, answer_filename)

        # write answer into json
        write_answer_json(function_snippet, write_directory, bug_id, answer_filename)


def build_prompt(bug_info, selected_features: List[str]):
    prompt_template = json.load(open("prompt_template.json", "r"))

    prompt = f"""{prompt_template["preface"]}

{prompt_template["buggy_code_blocks"]}
"""

    for code_block in bug_info["buggy_code_blocks"]:
        prompt = prompt + f"""
{code_block["source_code"]}


"""

    features = bug_info["features"]

    if "class_definition" in selected_features:
        prompt = prompt + f"""
{prompt_template["class_definition"]}

{features["class_definition"]}


"""

    if "variable_definitions" in selected_features:
        prompt = prompt + f"""
{prompt_template["variable_definitions"]}

{features["variable_definitions"]}


"""

    if "error_message" in selected_features:
        prompt = prompt + f"""
{prompt_template["error_message"]}

{features["error_message"]}


"""

    if "stack_trace" in selected_features:
        prompt = prompt + f"""
{prompt_template["stack_trace"]}

{features["stack_trace"]}


"""

    if "test_code_blocks" in selected_features:
        for test in features["test_code_blocks"]:
            prompt = prompt + f"""
{prompt_template["test_code_blocks"]}

{test["test_code"]}


"""

    if "raised_issue_descriptions" in selected_features:
        for issue in features["raised_issue_descriptions"]:
            prompt = prompt + f"""
{prompt_template["raised_issue_descriptions"]}
{issue["title"]}

{issue["content"]}"""

    #     prompt = prompt + f"""
    # {prompt_template["constrain_conclusion"]}"""

    return prompt


def write_prompt(prompt: str, directory: str, bug_id: int, filename: str):
    makedirs(path.join(directory, str(bug_id)), exist_ok=True)
    with open(path.join(directory, str(bug_id), filename), "w") as prompt_file:
        prompt_file.write(prompt)


def write_answer_markdown(answer: str, directory: str, bug_id: int, filename: str):
    makedirs(path.join(directory, str(bug_id)), exist_ok=True)
    with open(path.join(directory, str(bug_id), filename + ".md"), "w") as answer_file:
        answer_file.write(answer)


def write_answer_json(code_snippets: str, directory: str, bug_id: int, filename: str):
    makedirs(path.join(directory, str(bug_id)), exist_ok=True)
    global database, project

    data_info_address = path.join("..", "database", database, "bugs-info", project + ".json")

    with open(data_info_address, "r", encoding="utf-8") as read_json_file:
        bugs_data = json.load(read_json_file)

    info_list: List = bugs_data["bugs"]

    fix_line = None
    for bug in info_list:
        if bug["id"] == bug_id:
            fix_line = bug["fix_lines"][0]

    input_json = {
        project: [
            {
                "bugID": bug_id,
                "start_line": fix_line["start_line"],
                "file_name": fix_line["filename"],
                "replace_code": code_snippets
            }
        ]
    }

    with open(path.join(directory, str(bug_id), filename + ".json"), "w") as json_file:
        json.dump(input_json, json_file, indent=4)


def get_answer_from_chatgpt(prompt: str, llm_model: str):
    system_prompt = """Your role:
- Repair the program with a replacement that requires minimal changes to the source code.
- Ensure that the replacement allows the program to pass a failed test without affecting other successful tests.
- Make sure the fixed patch can be easily applied to the original project.
- Provide a complete code snippet as your response, representing a fully functional function.
"""

    # llm_model should be "gpt-4" or "gpt-3.5-turbo"
    try:
        chat_completion = openai.ChatCompletion.create(
            model=llm_model, messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        return chat_completion.choices[0].message.content

    # ignore if token length exceeds window size
    except Exception:
        return ""


if __name__ == "__main__":
    main()
