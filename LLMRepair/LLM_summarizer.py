import tiktoken
import pickle
from pathlib import Path
from gpt_utils import get_responses_from_prompt, QueryException
from utils import print_in_red, print_in_yellow, iter_bugid_folders, get_function_code, get_facts_in_prompt, get_import_statements
from typing import List


def get_response_and_store_results(prompt: str, prompt_file: Path, response_file: Path, pkl_file: Path, trials=1) -> List[str]:
    # if this prompt is too long just set bit to 0
    # we need to estimate tokens first
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(prompt))
    if num_tokens > 16000:
        raise QueryException(f"Prompt is exceeding 16000 tokens")

    gpt_response = get_responses_from_prompt(
        prompt=prompt,
        model="gpt-3.5-turbo-1106",
        trial=trials,
        temperature=1
    )
    responses: List[str] = gpt_response["responses"]

    # prompt file
    draft_md_content = "# Prompt\n"
    draft_md_content += f"{prompt}\n\n"
    prompt_file.write_text(draft_md_content)

    # response file
    draft_md_content = "# Response\n"
    for i, response in enumerate(responses):
        draft_md_content += f"## Response {i + 1}\n{response}\n\n"
    response_file.write_text(draft_md_content)

    # pkl file
    with open(pkl_file, "wb") as dump_pickle_file:
        pickle.dump(responses, dump_pickle_file)

    return responses


general_prompt_template = """
Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.

Assume that the following list of imports are available in the current environment, so you don't need to import them when generating a fix.
```python
{0}
```

The following is the buggy function that you need to fix:
```python
{1}
```

{2}
""".strip()

summarize_test_info_prompt_template = """
You task is to identify and output useful information from the a case code and an error message from a failed test case. 

{0}
""".strip()


# 7. Compile the Extracted Information: Output the findings in a structured format, including:
#     Overview: Test case name, objective, inputs, and expected outcomes.
#     Implementation: Examination of key operations, inputs, and desired results.
#     Error Breakdown: Detailed error message interpretation, with relevance to test case logic.

# Please output the following information in detail:
# 1. Identify the Test Case Code: Begin by identifying the test function or method within the specific block of code that represents the test case.
# 2. Analyze the Test Case Objective: Understand what the test case is intended to achieve. Look for comments or documentation within the code that explain its purpose, inputs, expected behavior, and output.
# 3. Examine the Test Case Implementation: Review the implementation details of the test case. Identify the key operations, the input values being tested, and how the expected result is defined within the code.
# 4. Locate the Error Message: Find the error message or output generated when the test case failed. This information is crucial for diagnosing the issue.
# 5. Analyze the Error Message: Break down the error message to understand its components. Look for specific error codes, descriptions of what went wrong, and any references to lines of code or specific conditions that were not met.
# 6. Map the Error to the Test Case: Relate the information in the error message back to the corresponding lines or logic in the test case code. This helps identify where the test did not behave as expected.

def main():
    database_folder_path = Path.cwd().parent / "training-data" / "LLM_summarizer"

    for bugid, project_folder, bugid_folder in iter_bugid_folders(database_folder_path):
        function_code = get_function_code(bugid_folder, bugid)
        import_statements = get_import_statements(bugid_folder)
        facts_in_prompt = get_facts_in_prompt(bugid_folder)
        class_info = facts_in_prompt["2"]
        file_info = facts_in_prompt["3"]
        test_info = facts_in_prompt["4"]
        dynamic_info = facts_in_prompt["5"]
        github_info = facts_in_prompt["6"]
        cot_instruction = facts_in_prompt["7"]

        print(bugid)
        print(test_info)

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(test_info))
        print(num_tokens)

        # get_response_and_store_results(prompt=summarize_test_info_prompt_template.format(test_info),
        #                                prompt_file=bugid_folder / "test_info_prompt.md",
        #                                response_file=bugid_folder / "test_info_response.md",
        #                                pkl_file=bugid_folder / "test_info_response.pkl")


if __name__ == "__main__":
    main()
