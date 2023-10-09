import argparse
import sys
import json
import subprocess
import os
from typing import Dict
import pandas as pd

sys.path.append('..')

prompt_type = ""
database = ""
model = ""


def main():
    parser = argparse.ArgumentParser(description="Generate result excel")
    parser.add_argument('-t', '--type', help="Prompt type, single: 0, multi: 1", required=True, type=int)
    parser.add_argument('-d', '--database', help="Database name, should be a folder name under the database directory",
                        type=str, required=True)
    parser.add_argument('-m', '--model', help="LLM model name, Should be 'gpt-4' or 'gpt-3.5-turbo'",
                        required=True, type=str)

    args = parser.parse_args()

    global prompt_type, database, model
    prompt_type = "single-prompt" if args.type == 0 else "multi-prompt"
    database = args.database
    model = args.model

    bug_list_address = os.path.join("..", "database", "subsets-list", args.database + ".json")
    bugs_list: Dict = json.load(open(bug_list_address, "r", encoding="utf-8"))

    data = {
        "Project": [],
        "Bug_id": [],
        "error_message": [],
        "test_code_blocks": [],
        "raised_issue_descriptions": [],
        "correct": []
    }
    for project in bugs_list.keys():
        for bug_id in bugs_list[project]:
            test_directory = os.path.join("..", "benchmarks", project, str(bug_id), "PyRepair",
                                          "benchmark_wrangling", "BugsInPy")
            results_directory = os.path.join("..", "prompt-results", prompt_type, database, model, project, str(bug_id))

            results_json = [f for f in os.listdir(results_directory) if f.endswith('.json')]

            for json_file in results_json:
                json_path = os.path.abspath(os.path.join(results_directory, json_file))

                run_test(test_directory, json_path)
                correct = get_test_result(test_directory)

                used_features = json.load(open(json_path, "r", encoding="utf-8"))["used_features"]

                data["Project"].append(project)
                data["Bug_id"].append(bug_id)
                data["error_message"].append(1 if "error_message" in used_features else 0)
                data["test_code_blocks"].append(1 if "test_code_blocks" in used_features else 0)
                data["raised_issue_descriptions"].append(1 if "raised_issue_descriptions" in used_features else 0)
                data["correct"].append(correct)

    excel_path = os.path.join("..", "prompt-results", prompt_type, database, model, database + "_" + model + ".xlsx")
    write_spreadsheet(data, excel_path)


def run_test(test_directory: str, json_path: str):
    try:
        command1 = ["python3.11", "run_custom_patch.py", json_path, "--output-dir", "."]
        result1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True,
                                 cwd=test_directory)
        print("Standard Output (Command 1):")
        print(result1.stdout)
    except Exception:
        pass


def get_test_result(test_directory: str) -> int:
    result: Dict = json.load(open(os.path.join(test_directory, "output_file.json"), "r", encoding="utf-8"))
    return next(iter(result.values()))


def write_spreadsheet(data: Dict, path: str):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)


if __name__ == "__main__":
    main()
