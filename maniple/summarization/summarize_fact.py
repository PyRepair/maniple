def resolve_related_functions(processor: Processor):
    if processor.facts_in_prompt["2"] == "" and processor.facts_in_prompt["3"] == "":
        log_red("No used function info")
        return ""

    related_functions_prompt = processor.related_functions_prompt
    num_tokens = count_tokens(related_functions_prompt)
    if num_tokens > 16_000:
        log_red(f"Related functions summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
        log("Preserving related functions. Tokens:", num_tokens)
        return related_functions_prompt

    log("Generating related functions summary. Tokens:", num_tokens, end=" ")
    related_functions_summary = get_response_and_store_results(prompt=related_functions_prompt,
                                                               prompt_file=processor.bug_folder / "related_functions_prompt.md",
                                                               response_file=processor.bug_folder / "related_functions_response.md",
                                                               pkl_file=processor.bug_folder / "related_functions_response.pkl")[0]
    log("->", count_tokens(related_functions_summary))

    result = "## Summary of Related Functions\n\n"
    result += related_functions_summary
    result += "\n\n\n"

    return result


def summarize_test_info(processor: Processor):
    if processor.facts_in_prompt["4"] == "" or processor.facts_in_prompt["5"] == "":
        log_red("No test info")
        return ""

    stacktrace_summary_prompt = processor.stack_trace_summary_prompt
    num_tokens = count_tokens(stacktrace_summary_prompt)
    if num_tokens > 16_000:
        log_red(f"Test info summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
        log("Preserving test info. Tokens:", num_tokens)
        return processor.facts_in_prompt["5"]

    log("Generating test info. Tokens:", count_tokens(stacktrace_summary_prompt), end=" ")
    error_message_summary = get_response_and_store_results(prompt=stacktrace_summary_prompt,
                                                           prompt_file=processor.bug_folder / "test_info_prompt.md",
                                                           response_file=processor.bug_folder / "test_info_response.md",
                                                           pkl_file=processor.bug_folder / "test_info_response.pkl")[0]
    log("->", count_tokens(error_message_summary))

    result = "## Summary of the test cases and error messages\n\n"
    result += error_message_summary
    result += "\n\n\n"

    return result


def resolve_runtime_value(processor: Processor):
    if processor.facts_in_prompt["6"] == "":
        log_red("No runtime value")
        return ""

    runtime_value_prompt = processor.runtime_value_prompt
    num_tokens = count_tokens(runtime_value_prompt)
    if num_tokens > 16_000:
        log_red(f"Runtime value summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
        log("Preserving runtime value. Tokens:", num_tokens)
        return processor.facts_in_prompt["6"]

    log("Generating runtime value summary. Tokens:", num_tokens, end=" ")
    runtime_value_summary = get_response_and_store_results(prompt=runtime_value_prompt,
                                                           prompt_file=processor.bug_folder / "runtime_info_prompt.md",
                                                           response_file=processor.bug_folder / "runtime_info_response.md",
                                                           pkl_file=processor.bug_folder / "runtime_info_response.pkl")[0]
    log("->", count_tokens(runtime_value_summary))

    result = "## Summary of Runtime Variables and Types in the Buggy Function\n\n"
    result += runtime_value_summary
    result += "\n\n\n"

    return result


def resolve_angelic_value(processor: Processor):
    if processor.facts_in_prompt["7"] == "":
        log_red("No angelic value")
        return ""

    angelic_value_prompt = processor.angelic_value_prompt
    num_tokens = count_tokens(angelic_value_prompt)
    if num_tokens > 16_000:
        log_red(f"Angelic value summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
        log("Preserving angelic value. Tokens:", num_tokens)
        return processor.facts_in_prompt["7"]

    log("Generating angelic value summary. Tokens:", num_tokens, end=" ")
    angelic_value_summary = get_response_and_store_results(prompt=angelic_value_prompt,
                                                           prompt_file=processor.bug_folder / "angelic_info_prompt.md",
                                                           response_file=processor.bug_folder / "angelic_info_response.md",
                                                           pkl_file=processor.bug_folder / "angelic_info_response.pkl")[0]
    log("->", count_tokens(angelic_value_summary))

    result = "## Summary of Expected Parameters and Return Values in the Buggy Function\n\n"
    result += angelic_value_summary
    result += "\n\n\n"

    return result


def resolve_github_issue(processor: Processor):
    if processor.facts_in_prompt["8"] == "":
        log_red("No GitHub issue")
        return ""

    github_issue_prompt = processor.issue_description_prompt
    num_tokens = count_tokens(github_issue_prompt)
    if num_tokens > 16_000:
        log_red(f"GitHub issue summary is too long. Tokens: {num_tokens}")
        return ""

    if num_tokens < COMPRESSION_CAP:
        log("Preserving GitHub issue. Tokens:", num_tokens)
        return processor.facts_in_prompt["8"]

    log("Generating GitHub issue summary. Tokens:", num_tokens, end=" ")
    github_issue_summary = get_response_and_store_results(prompt=github_issue_prompt,
                                                          prompt_file=processor.bug_folder / "github_issue_prompt.md",
                                                          response_file=processor.bug_folder / "github_issue_response.md",
                                                          pkl_file=processor.bug_folder / "github_issue_response.pkl")[0]
    log("->", count_tokens(github_issue_summary))

    result = "## Summary of the GitHub Issue Related to the Bug\n\n"
    result += github_issue_summary
    result += "\n\n\n"

    return result

