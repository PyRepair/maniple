import argparse
import json
import os

from utils import print_in_red, print_in_yellow
from openai import OpenAI

from gpt_utils import GPTConnection, get_response_from_prompt, QueryException

client = OpenAI(api_key="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")


class PromptGenerator:
    def __init__(self, database_dir: str, project_name: str, bug_id: str):
        self.output_dir: str = os.path.join(database_dir, project_name, bug_id)

        with open(os.path.join(self.output_dir, "facts-in-prompt.json"), "r") as facts_text_file:
            self.facts_text: dict = json.load(facts_text_file)

        facts_path = os.path.join(self.output_dir, "facts.json")
        with open(facts_path, "r") as facts_file:
            self.facts: dict = json.load(facts_file)

        with open(os.path.join(self.output_dir, "bug-data.json"), "r") as bug_data_file:
            bug_data: dict = next(iter(json.load(bug_data_file).values()))
            user_dir: str = list(bug_data)[0]
            self.buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
            self.buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]
            self.buggy_function_source_code: str = bug_data[user_dir]["buggy_functions"][0]["function_code"]

            prefix = f"{project_name}_{bug_id}"
            start_idx = user_dir.find(prefix) + len(prefix) + 1
            self.buggy_location_file_name = user_dir[start_idx:]

        self.project_name = project_name
        self.bug_id = bug_id

        self.prompt: str = ""
        self.report: str = ""

        self.max_generation_count = 10
        self.max_conversation_count = 3

        self.generate_prompt()

    def generate_prompt(self):
        self.prompt = f"""You have been provided with the following source code for a buggy function, along with fact sections containing titles that describe the facts. Suppose you are a helpful pair programming buddy who is writing a bug report to your colleague, who will fix this bug. Your role is to provide useful facts that can help fix this bug in your report. Please note that your responsibility is limited to selecting useful facts.

# The source code of the buggy function
```python
{self.buggy_function_source_code}
```

{self.facts_text["2"]}

{self.facts_text["3"]}

{self.facts_text["4"]}

{self.facts_text["5"]}

{self.facts_text["6"]}
"""

    def write_report_prompt(self):
        with open(os.path.join(self.output_dir, "bug_report_prompt.md"), "w", encoding="utf-8") as prompt_file:
            prompt_file.write(self.prompt)

    def get_report_response(self, trial, model):
        try:
            response = get_response_from_prompt(self.prompt, model)
            response_content = response["response"]
            with open(os.path.join(self.output_dir, f"bug_report_{trial}.md"), "w", encoding="utf-8") as report_file:
                report_file.write(response_content)

        except QueryException as error:
            print_in_yellow(f"{self.project_name}-{self.bug_id}: {error}")

        except Exception as error:
            print_in_red(f"{self.project_name}-{self.bug_id}: {error}")

    def build_prompt_from_report(self, report_content):
        self.report = f"""You are an experienced software engineer working with your team to fix a buggy function. The source code of this buggy function is listed below. Your helpful colleague has written a bug report for you, and your task is to analyze this bug report and propose fixes. Assuming that the corrected function will be used to replace the original buggy function, you should provide the complete corrected function code.

# The source code of the buggy function
```python
{self.buggy_function_source_code}
```

# Bug report
{report_content}
"""

    def get_fix_patch_from_report(self, count_number: int, gpt_model: str):
        try:
            with open(os.path.join(self.output_dir, f"bug_report_{count_number}.md"), "r") as report_file:
                self.build_prompt_from_report(report_file.read())

        except FileNotFoundError:
            return

        file_prefix = "bug_report"

        response_md_file_name = file_prefix + "_response_" + str(count_number) + ".md"
        response_json_file_name = file_prefix + "_response_" + str(count_number) + ".json"

        response_md_file_path = os.path.join(self.output_dir, response_md_file_name)
        response_json_file_path = os.path.join(self.output_dir, response_json_file_name)

        try:
            gpt_connection = GPTConnection()
            response: dict = gpt_connection.get_response_with_fix_path(self.report, gpt_model, self.facts["1.1.1"],
                                                                       self.buggy_function_name)

            # print(f"{self.project_name}-{self.bug_id} remain count: {gpt_connection.max_generation_count} and {gpt_connection.max_conversation_count}")

            with open(response_md_file_path, "w", encoding="utf-8") as response_md_file:
                response_md_file.write(response["response"])

            with open(response_json_file_path, "w", encoding="utf-8") as response_json_file:
                test_input_data = {
                    self.project_name: [
                        {
                            "bugID": int(self.bug_id),
                            "start_line": self.buggy_function_start_line,
                            "file_name": self.buggy_location_file_name,
                            "replace_code": response["replace_code"],
                            "import_list": response["import_statements"]
                        }
                    ]
                }
                json.dump(test_input_data, response_json_file, indent=4)

        except QueryException as error:
            print_in_yellow(f"{self.project_name}-{self.bug_id}: {error}")

        except Exception as error:
            print_in_red(f"{self.project_name}-{self.bug_id}: {error}")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--database",
        type=str,
        help="specify a database name under training-data folder",
        required=True
    )
    args_parser.add_argument(
        "--trial",
        type=int,
        help="how many responses you want get from one prompt",
        required=True
    )

    args = args_parser.parse_args()

    trial_count = args.trial

    database_path = os.path.join("..", "training-data", args.database)

    for project in os.listdir(database_path):
        project_path = os.path.join(database_path, project)

        if not os.path.isdir(project_path):
            continue

        for bid in os.listdir(project_path):
            bug_path = os.path.join(project_path, bid)

            prompt_generator = PromptGenerator(database_path, project, bid)
            prompt_generator.write_report_prompt()

            prompt_generator.get_report_response(trial_count, "gpt-3.5-turbo-1106")
            prompt_generator.get_fix_patch_from_report(trial_count, "gpt-3.5-turbo-1106")
