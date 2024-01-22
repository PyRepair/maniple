import time

import openai
from openai import OpenAI

from utils import estimate_function_code_length, print_in_red, print_in_yellow, \
    extract_function_and_imports_from_code_block, find_patch_from_response
from prompt_generator import num_tokens_from_string

client = OpenAI(api_key="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")


class GPTConnection:
    def __init__(self):
        self.max_generation_count = 10
        self.max_conversation_count = 3
        self.buggy_function_name = ""

    def get_response_with_fix_path(self, prompt: str, gpt_model: str, source_buggy_function: str,
                                   buggy_function_name: str) -> dict:
        self.max_generation_count = 10
        self.max_conversation_count = 3
        self.buggy_function_name = buggy_function_name

        buggy_function_length = estimate_function_code_length(source_buggy_function)
        messages = [{"role": "user", "content": prompt}]

        response = self.get_response_with_valid_patch(messages, gpt_model)

        conversation_response = response
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response["response"]},
            {"role": "user", "content": "Print the full code of the fixed function"},
        ]

        while estimate_function_code_length(conversation_response["fix_patch"]) < 0.6 * buggy_function_length:
            conversation_response = self.get_response_with_valid_patch(messages, gpt_model)

            self.max_conversation_count -= 1
            if self.max_conversation_count == 0:
                raise QueryException("Exceed max conversation count")

        return conversation_response

    def get_response_with_valid_patch(self, messages: list, gpt_model: str) -> dict:
        while self.max_generation_count > 0:
            response = get_response_from_messages(messages, gpt_model)
            fix_patch = find_patch_from_response(response["response"], self.buggy_function_name)
            if fix_patch is not None:
                response["fix_patch"] = fix_patch
                replace_code, import_statements = extract_function_and_imports_from_code_block(fix_patch,
                                                                                               self.buggy_function_name)
                if replace_code is not None:
                    response["replace_code"] = replace_code
                    response["import_statements"] = import_statements
                    return response

            self.max_generation_count -= 1

        raise QueryException("Exceed max generation count")


def get_response_from_messages(messages: list, model: str) -> dict:
    for message in messages:
        num_tokens = num_tokens_from_string(message["content"], "cl100k_base")
        if num_tokens > 16385:
            raise QueryException(f"{num_tokens} exceed maximum 16385 token size")

    retry_max_count = 5
    while retry_max_count > 0:
        try:
            time.sleep(0.2)
            chat_completion = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            finish_reason = chat_completion.choices[0].finish_reason
            if finish_reason == "length":
                raise QueryException("Exceed maximum 16385 token size")

            if finish_reason != "stop":
                print_in_yellow(f"retrying due to not stop, finish reason: {finish_reason}")
                retry_max_count -= 1
                continue

            if chat_completion.choices[0].message.content != "":
                return {
                    "response": chat_completion.choices[0].message.content,
                    "prompt_completion": (messages, chat_completion)
                }

            retry_max_count -= 1

        except openai.RateLimitError:
            print_in_yellow("Meet ratelimit error, wait for 5 seconds")
            time.sleep(5)
            retry_max_count -= 1

    raise QueryException("Tried 5 times still fail to get response")


def get_response_from_prompt(prompt: str, model: str) -> dict:
    messages = [{"role": "user", "content": prompt}]

    return get_response_from_messages(messages, model)


class QueryException(Exception):
    pass
