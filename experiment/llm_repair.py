from typing import Dict
from bug_type import ProjectData, ProjectInfo
import argparse

import openai
import sys
import json
from os import path
sys.path.append('..')


openai.api_key = "rg-B09kO5jDDdG0axfeuA5YP0LLTX8Fxi0rxNrgtzU6ZfiPRVNE"
openai.api_base = "https://ai.redgatefoundry.com/v1"


def main():
    parser = argparse.ArgumentParser(description="Create prompt and write result")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--database',
                       help="Database name, should be a folder under database directory", required=True, type=str)
    group.add_argument('-p', '--project', help="Project name", required=True, type=str)
    parser.add_argument('-t', '--type', help="Prompt type, single: 0, multi: 1", required=True, type=int)
    group.add_argument('-f', '--feature_split',
                       help="Split the features, drop one feature every run", required=True, type=str)

    args = parser.parse_args()

    if args.database:
        print(args.database)
    if args.project:
        print(args.project)
    if args.type:
        print(args.type)
    if args.feature_split:
        print(args.feature_split)

    # load project data form database
    # project_name = args[0]
    # data_address = path.join("..", "database", "bugs-data", project_name + ".json")
    # bugs_data: ProjectData = json.load(open(data_address, "r"))

    # traversal whole dataset, generate prompt and answer for every bug, and drop only one feature once
    # traversal_bugs(bugs_data)


def traversal_bugs(bugs_data: ProjectData):
    project_name = bugs_data["project"]
    for bug_index in range(len(bugs_data["bugs"])):
        bug_id = bugs_data["bugs"][bug_index]["id"]

        # only use avaialable features
        exist_features = []
        exist_feature_indeces = []

        feature_index = 0
        for feature in bugs_data["bugs"][bug_index]:
            if feature == "id" or feature == "source_code":
                feature_index += 1
                continue
            if bugs_data["bugs"][bug_index][feature] is not None:
                exist_features.append(feature)
                exist_feature_indeces.append(feature_index)
                feature_index += 1

        # run with all features
        generate_answers(bugs_data["bugs"][bug_index], exist_features, exist_feature_indeces, project_name, bug_id)

        # drop only one feature once
        for drop_index in range(len(exist_features)):
            selected_features = exist_features.copy()
            selected_features.pop(drop_index)
            selected_indeces = exist_feature_indeces.copy()
            selected_indeces.pop(drop_index)

            generate_answers(bugs_data["bugs"][bug_index], selected_features, selected_indeces, project_name, bug_id)


def generate_answers(features, selected_features, selected_indeces, project_name, bug_id):
    prompt_filename = "prompt-"
    answer_filename = "answer-"
    for selected_index in selected_indeces:
        prompt_filename += str(selected_index)
        answer_filename += str(selected_index)
    prompt_filename += ".md"
    answer_filename += ".md"

    # Build prompt from template
    prompt = build_prompt(features, selected_features)

    # write prompt into md file
    write_prompt(prompt, project_name, bug_id, prompt_filename)

    # connect to chatgpt to get answer
    answer = get_answer_from_chatgpt(prompt)

    # write answer into md file
    write_answer(answer, project_name, bug_id, answer_filename)


def build_prompt(features, selected_features):
    prompt_template = json.load(open("prompt_template.json", "r"))

    prompt = f"""{prompt_template["preface"]}

{prompt_template["source_code"]}

{features["source_code"]}


"""

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

    if "test_code" in selected_features:
        prompt = prompt + f"""
{prompt_template["test_code"]}

{features["test_code"]}


"""

    if "raised_issue_description" in selected_features:
        prompt = prompt + f"""
{prompt_template["raised_issue_description"]} '{features["raised_issue_description"]}'.


"""

    prompt = prompt + f"""
{prompt_template["constrain_conclusion"]}"""

    return prompt


def write_prompt(prompt, project_name, bug_id, filename):
    prompt_fileaddress = "./" + project_name + "/" + str(bug_id) + "/" + filename
    with open(prompt_fileaddress, "w") as promptfile:
        promptfile.write(prompt)


def write_answer(answer, project_name, bug_id, filename):
    answer_fileaddress = "./" + project_name + "/" + str(bug_id) + "/" + filename
    with open(answer_fileaddress, "w") as answerfile:
        answerfile.write(answer)


def get_answer_from_chatgpt(prompt):
    model = "gpt-4"  # "gpt-4" or "gpt-3.5-turbo"

    system_prompt = "You role is to fix program"

    chat_completion = openai.ChatCompletion.create(
        model=model, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    main()
