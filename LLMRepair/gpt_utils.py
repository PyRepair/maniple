import json
import math
import os
import pickle
import time
from pathlib import Path

import openai
import tiktoken
from openai import OpenAI

from utils import estimate_function_code_length, print_in_red, print_in_yellow, \
    extract_function_and_imports_from_code_block, find_patch_from_response

client = OpenAI(api_key="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")


def get_and_save_response_with_fix_path(prompt: str, gpt_model: str, response_file_name_prefix: str, database_dir: Path,
                                        project_name: str, bug_id: str, trial: int, data_to_store: dict = None) -> dict:
    output_dir: str = str(database_dir / project_name / bug_id)

    with open(os.path.join(output_dir, "bug-data.json"), "r") as bug_data_file:
        bug_data: dict = next(iter(json.load(bug_data_file).values()))
        user_dir: str = list(bug_data)[0]
        buggy_function_name: str = bug_data[user_dir]["buggy_functions"][0]["function_name"]
        buggy_function_start_line: str = bug_data[user_dir]["buggy_functions"][0]["start_line"]
        # buggy_function_source_code: str = bug_data[user_dir]["buggy_functions"][0]["function_code"]

        prefix = f"{project_name}_{bug_id}"
        start_idx = user_dir.find(prefix) + len(prefix) + 1
        buggy_location_file_name = user_dir[start_idx:]

    responses = None
    try:
        responses = GPTConnection().get_response_with_fix_path(prompt, gpt_model, trial, buggy_function_name)
    except QueryException as error:
        error_str = str(error)
        print_in_yellow(error_str)
    except Exception as error:
        error_str = str(error)
        print_in_red(error_str)

    for index in range(trial):
        file_index = index + 1
        response_md_file_name = response_file_name_prefix + "_response_" + str(file_index) + ".md"
        response_json_file_name = response_file_name_prefix + "_response_" + str(file_index) + ".json"

        response_md_file_path = os.path.join(output_dir, response_md_file_name)
        response_json_file_path = os.path.join(output_dir, response_json_file_name)

        if responses is not None:
            response = responses["responses"][index]

            with open(response_md_file_path, "w", encoding='utf-8') as md_file:
                md_file.write(response["response"])

            with open(response_json_file_path, "w", encoding='utf-8') as json_file:
                test_data = {
                    "bugID": int(bug_id),
                    "start_line": buggy_function_start_line,
                    "file_name": buggy_location_file_name,
                    "replace_code": response["replace_code"],
                    "import_list": response["import_list"]
                }

                if data_to_store is not None:
                    test_data = {**data_to_store, **test_data}

                test_input_data = {
                    project_name: [test_data]
                }
                json.dump(test_input_data, json_file, indent=4)

            print(f"write response to {response_md_file_path}")

        else:
            with open(response_md_file_path, "w", encoding='utf-8') as md_file:
                md_file.write(error_str)

            with open(response_json_file_path, "w", encoding='utf-8') as json_file:
                test_data = {
                    "bugID": int(bug_id),
                    "start_line": buggy_function_start_line,
                    "file_name": buggy_location_file_name,
                    "replace_code": None,
                    "import_list": []
                }

                if data_to_store is not None:
                    test_data = {**data_to_store, **test_data}

                test_input_data = {
                    project_name: [test_data]
                }
                json.dump(test_input_data, json_file, indent=4)

            print_in_yellow(f"write response error to {response_md_file_path}")

    if responses is not None:
        completion_file_name = response_file_name_prefix + "_completion" + ".pkl"
        completion_file_path = os.path.join(output_dir, completion_file_name)

        with open(completion_file_path, 'wb') as completion_file:
            pickle.dump((responses["prompt_messages"], responses["response_completions"]), completion_file)

        return responses["total_token_usage"]

    else:
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }




class GPTConnection:
    def __init__(self):
        self.max_generation_count = 3
        # self.max_conversation_count = 3
        self.buggy_function_name = ""

    def get_response_with_fix_path(self, prompt: str, gpt_model: str, trial: int, buggy_function_name: str) -> dict:
        self.max_generation_count = 3
        self.buggy_function_name = buggy_function_name

        # buggy_function_length = estimate_function_code_length(source_buggy_function)
        messages = [{"role": "user", "content": prompt}]

        responses = self.get_response_with_valid_patch(messages, gpt_model, trial)

        # for index in range(len(responses["responses"])):
        #     response: dict = responses["responses"][index]
        #
        #     conversation_response = response
        #     messages = [
        #         {"role": "user", "content": prompt},
        #         {"role": "assistant", "content": response["response"]},
        #         {"role": "user", "content": "Print the full code of the fixed function"},
        #     ]
        #
        #     self.max_conversation_count = 3
        #     self.max_generation_count = 6
        #
        #     start_time = time.time()
        #
        #     while True:
        #         if estimate_function_code_length(conversation_response["fix_patch"]) > 0.6 * buggy_function_length:
        #             responses["responses"][index] = conversation_response
        #             break
        #
        #         conversation_responses = self.get_response_with_valid_patch(messages, gpt_model, trial=1)
        #         responses["total_token_usage"] = combine_token_usage(responses["total_token_usage"], conversation_responses["total_token_usage"])
        #
        #         if len(conversation_responses["responses"]) > 0:
        #             conversation_response = conversation_responses["responses"][0]
        #
        #         self.max_conversation_count -= 1
        #         if self.max_conversation_count == 0:
        #             print_in_yellow("Exceed max conversation count")
        #             break
        #
        #     end_time = time.time()
        #     if end_time - start_time > 120:
        #         print_in_red(f"long time for conversation")
        #         print(end_time - start_time)

        if len(responses["responses"]) < trial:
            for _ in range(trial - len(responses["responses"])):
                responses["responses"].append({
                    "response": "Run out of generation count",
                    "fix_patch": None,
                    "replace_code": None,
                    "import_list": []
                })

        assert len(responses["responses"]) == trial

        return responses

    def get_response_with_valid_patch(self, messages: list, gpt_model: str, trial: int) -> dict:
        start_time = time.time()

        responses = _get_responses_from_messages(messages, gpt_model, math.ceil(trial * 1.5))
        responses["prompt_messages"] = messages
        responses["responses"] = [{"response": value} for value in responses["responses"] if find_patch_from_response(value, self.buggy_function_name) is not None]

        while self.max_generation_count > 0:
            if len(responses["responses"]) >= trial:
                responses["responses"] = responses["responses"][:trial]

                for response in responses["responses"]:
                    fix_patch = find_patch_from_response(response["response"], self.buggy_function_name)
                    response["fix_patch"] = fix_patch
                    replace_code, import_list = extract_function_and_imports_from_code_block(fix_patch, self.buggy_function_name)
                    response["replace_code"] = replace_code
                    response["import_list"] = import_list

                end_time = time.time()
                if end_time - start_time > 60:
                    print_in_red(f"long time for generation")
                    print(end_time - start_time)

                return responses

            self.max_generation_count -= 1

            next_query_responses = _get_responses_from_messages(messages, gpt_model, trial)
            next_query_responses["responses"] = [{"response": value} for value in next_query_responses["responses"] if find_patch_from_response(value, self.buggy_function_name) is not None]
            responses["total_token_usage"] = combine_token_usage(responses["total_token_usage"], next_query_responses["total_token_usage"])

            if len(next_query_responses["responses"]) > 0:
                responses["responses"] = responses["responses"] + next_query_responses["responses"]
                responses["response_completions"] = responses["response_completions"] + next_query_responses["response_completions"]

        if len(responses["responses"]) > 0:
            print_in_yellow(f"Tried {str(self.max_generation_count)} times still fail to get enough responses")
            responses["responses"] = responses["responses"][:trial]

            for response in responses["responses"]:
                fix_patch = find_patch_from_response(response["response"], self.buggy_function_name)
                response["fix_patch"] = fix_patch
                replace_code, import_list = extract_function_and_imports_from_code_block(fix_patch, self.buggy_function_name)
                response["replace_code"] = replace_code
                response["import_list"] = import_list

            return responses


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def combine_token_usage(usage_1, usage_2) -> dict:
    if not isinstance(usage_1, dict):
        usage_1 = {
            "prompt_tokens": usage_1.prompt_tokens,
            "completion_tokens": usage_1.completion_tokens,
            "total_tokens": usage_1.total_tokens
        }

    if not isinstance(usage_2, dict):
        usage_2 = {
            "prompt_tokens": usage_2.prompt_tokens,
            "completion_tokens": usage_2.completion_tokens,
            "total_tokens": usage_2.total_tokens
        }

    return {
        "prompt_tokens": usage_1["prompt_tokens"] + usage_2["prompt_tokens"],
        "completion_tokens": usage_1["completion_tokens"] + usage_2["completion_tokens"],
        "total_tokens": usage_1["total_tokens"] + usage_2["total_tokens"]
    }


def get_responses_from_messages(messages: list, model: str, trial: int, retry_max_count: int = 4, default_safe: bool = False, temperature: float = 1.0) -> dict:
    responses = _get_responses_from_messages(messages, model, math.ceil(trial * 1.5), temperature=temperature)
    responses["prompt_messages"] = messages

    while retry_max_count > 0:
        retry_max_count -= 1

        if len(responses["responses"]) >= trial:
            responses["responses"] = responses["responses"][:trial]
            return responses

        next_query_responses = _get_responses_from_messages(messages, model, trial, temperature=temperature)
        responses["responses"] = responses["responses"] + next_query_responses["responses"]
        responses["response_completions"] = responses["response_completions"] + next_query_responses["response_completions"]
        responses["total_token_usage"] = combine_token_usage(responses["total_token_usage"], next_query_responses["total_token_usage"])

    if default_safe:
        return responses

    else:
        raise QueryException(f"Tried {str(retry_max_count)} times still fail to get enough responses")


def _get_responses_from_messages(messages: list, model: str, trial: int, temperature: float = 1.0) -> dict:
    for message in messages:
        num_tokens = num_tokens_from_string(message["content"], "cl100k_base")
        if num_tokens > 16385:
            raise QueryException(f"{num_tokens} exceed maximum 16385 token size")

    responses = {
        "responses": [],
        "response_completions": [],
        "total_token_usage": None
    }

    try:
        time.sleep(0.1)
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            n=trial,
            temperature=temperature
        )

        for choice in chat_completion.choices:
            finish_reason = choice.finish_reason
            if finish_reason == "length":
                raise QueryException("Exceed maximum 16385 token size")

            if finish_reason != "stop":
                print_in_yellow(f"drop 1 response due to not stop, finish reason: {finish_reason}")
                continue

            if choice.message.content != "":
                responses["responses"].append(choice.message.content)

        responses["response_completions"].append(chat_completion)
        responses["total_token_usage"] = chat_completion.usage

    except openai.RateLimitError:
        print_in_yellow("Meet ratelimit error, wait for 5 seconds")
        time.sleep(5)

    # print(f"finish {str(trial)} response generation")
    # print(len(responses["responses"]))

    return responses


def get_responses_from_prompt(prompt: str, model: str, trial: int, temperature: float = 1.0) -> dict:
    messages = [{"role": "user", "content": prompt}]

    return get_responses_from_messages(messages, model, trial, temperature=temperature)


class QueryException(Exception):
    pass
