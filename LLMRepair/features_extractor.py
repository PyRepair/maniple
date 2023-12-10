import ast
import os
import json
import re
from typing import Any, List, Optional, Tuple

from command_runner import (
    ensure_clone_and_prep_complete,
    run_extract_features_command,
)

from utils import (
    IGNORED_BUGS,
    NotSupportedError,
    generate_contextual_diff_with_char_limit,
    get_fact_map,
    print_in_red,
    print_in_yellow,
)


class Facts:
    """
    This class will parse the output from `bgp extract_features` tool and
    process the facts in a way that can be eaily used to construct a prompt
    """

    def __init__(self, bugid: str, bug_working_directory: str) -> None:
        self.facts = dict[str, Any]()
        self.stats = dict[str, List[Any]]()
        self._bugid = bugid
        self._bwd = bug_working_directory
        self._variables_in_methods = []

        self.FACT_MAP = get_fact_map()

        for key in self.FACT_MAP.keys():
            self.facts[key] = None

    def _log_stat(self, state_category, state_record):
        if self.stats.get(state_category) is None:
            self.stats[state_category] = [state_record]
        else:
            self.stats[state_category].append(state_record)

    def load_from_json_object(self, bug_record: dict) -> None:
        """
        The command `bgp extract_features ...` returns a JSON object with following schema:

        ```json
        {
            "youtube-dl:28": { "buggy_file_path": { ... } }
        }
        ```

        This method only concerns the fact per bug, the expected format for bug_record would be:

        ```json
        {
            "buggy_file_path1": { ... },
            "buggy_file_path2": { ... }
        }
        ```
        """
        if len(bug_record) > 2:
            raise NotSupportedError(
                "multiple buggy files are not supported at the moment"
            )

        for filename, file_info in bug_record.items():
            if filename == "test_data":
                for test_data in file_info:
                    self._resolve_test_data(test_data)
            else:
                self._resolve_file_info(filename, file_info)

    def _resolve_file_info(self, filename, file_info):
        self.facts["1.3.1"] = filename

        buggy_functions = []
        for bg_fn_info in file_info["buggy_functions"]:
            if bg_fn_info["function_code"] is not None:
                buggy_functions.append(bg_fn_info)

        if len(buggy_functions) > 1:
            raise NotSupportedError(
                "multiple buggy functions are not supported at the moment"
            )

        for buggy_function_info in buggy_functions:
            self._resolve_buggy_function(buggy_function_info)

        called_in_scope_functions = []
        in_scope_functions = file_info["inscope_functions"]
        in_scope_function_signatures = file_info["inscope_function_signatures"]
        for idx, fn in enumerate(in_scope_functions):
            if self._is_this_func_called(fn):
                called_in_scope_functions.append(in_scope_function_signatures[idx])
        if len(called_in_scope_functions) > 0:
            self.facts["1.3.2"] = called_in_scope_functions

    def _is_this_func_called(self, sig):
        for v in self._variables_in_methods:
            var = v.split(".")[-1]
            if Facts._extract_single_function_name(sig) == var:
                return True
        return False

    @staticmethod
    def _extract_single_function_name(function_code: str):
        """
        Extracts and returns the name of a single function from its source code.

        Args:
            function_code (str): A string containing the source code of a single function.

        Returns:
            str: The name of the function, or an empty string if no function name is found.
        """

        class SingleFunctionExtractor(ast.NodeVisitor):
            def __init__(self):
                self.name = ""

            def visit_FunctionDef(self, node):
                if self.name == "":
                    self.name = node.name

        try:
            tree = ast.parse(function_code)
            extractor = SingleFunctionExtractor()
            extractor.visit(tree)
            return extractor.name
        except SyntaxError:
            return ""  # Return an empty string in case of a syntax error

    def _resolve_buggy_function(self, buggy_function_info):
        buggy_function = buggy_function_info["function_code"]
        buggy_function_docstring = buggy_function_info["docstring"]

        if buggy_function is not None:
            self.facts["1.1.1"] = Facts.remove_docstring_from_source(buggy_function)
        else:
            print_in_red("FATAL: the buggy function does not exist")

        if buggy_function_docstring is not None:
            self.facts["1.1.2"] = buggy_function_docstring

        self._variables_in_methods = buggy_function_info["filtered_variables"]

        if buggy_function_info["class_data"] is not None:
            self._resolve_class_info(buggy_function_info["class_data"])

        # angelic variables
        self._resolve_angelic_variables(buggy_function_info)

    def _get_angelic_dynamics_LEGACY(self, function_info):
        if function_info.get("angelic_variable_values") is None:
            buggy_variables_values = []
        else:
            buggy_variables_values = function_info["variable_values"]

        if function_info.get("angelic_variable_values") is None:
            angelic_variable_values = []
        else:
            angelic_variable_values = function_info["angelic_variable_values"]

        iovals = []
        iotypes = []

        matched_buggy_variable_indices = set()
        for angelic_idx, angelic_IO_tuple in enumerate(angelic_variable_values):
            containEqual = False
            for buggy_idx, buggy_IO_tuple in enumerate(buggy_variables_values):
                # if same input got matched, then we can use this pair
                # we also did a sanity check to make sure the output is not empty and having same keys
                if (
                    buggy_IO_tuple[0] == angelic_IO_tuple[0]
                    and len(buggy_IO_tuple[1].keys()) > 0
                    and buggy_IO_tuple[1].keys() == angelic_IO_tuple[1].keys()
                ):
                    containEqual = True
                    break

            # if same input got matched, then we can use this pair, otherwise we discard it
            if not containEqual or buggy_idx in matched_buggy_variable_indices:  # type: ignore
                continue

            # if the the buggy program crash, the IO tuple will be incomplete and we should ignore it
            if len(buggy_IO_tuple) < 2 or len(buggy_IO_tuple[1].keys()) == 0:  # type: ignore
                continue
            if len(angelic_IO_tuple) < 2 or len(angelic_IO_tuple[1].keys()) == 0:
                continue

            # now we have a pair of buggy and angelic IO tuple
            # ready to use pair (buggy_IO_tuple and angelic_IO_tuple)
            # Next step: filter buildin method and None for input
            i_val = dict()
            i_type = dict()
            for varName, varItem in angelic_IO_tuple[0].items():
                if self._does_this_variable_record_contains_non_empty_value(varItem):
                    i_val[varName] = {
                        "variable_value": varItem["variable_value"],
                    }
                    i_type[varName] = {
                        "variable_type": varItem["variable_type"],
                    }

            # Next step: work with output
            # merge buggy_IO_tuple[1] and angelic_IO_tuple[1]
            # and also filter out None or builtin method
            # and also generate diff
            o_val = dict()
            o_type = dict()
            for varName, varItem in angelic_IO_tuple[1].items():
                buggyItem = buggy_IO_tuple[1][varName]  # type: ignore
                if self._does_this_variable_record_contains_non_empty_value(
                    varItem
                ) and self._does_this_2_variable_records_actually_have_changes(
                    buggyItem, varItem
                ):
                    buggy_value = buggyItem["variable_value"]
                    angelic_value = varItem["variable_value"]
                    value_diff = generate_contextual_diff_with_char_limit(
                        buggy_value, angelic_value
                    )
                    o_val[varName] = {
                        "buggy_value": buggy_value,
                        "angelic_value": angelic_value,
                        "diff": value_diff,
                    }
                    o_type[varName] = {"variable_type": varItem["variable_type"]}

            if len(i_val.keys()) == 0 or len(o_val.keys()) == 0:
                continue

            # if the data survive util the last time, then we can add the buggy_idx to the set
            matched_buggy_variable_indices.add(buggy_idx)  # type: ignore
            self._log_stat(
                "buggy_angelic_dynamics_pair",
                (buggy_idx, angelic_idx),  # type: ignore
            )

            # now we have target_output and target_input
            # put them in pair and add to result_set
            iovals.append((i_val, o_val))
            iotypes.append((i_type, o_type))

        return (iovals, iotypes)

    def _resolve_dynamics_value_and_type(self, varItem) -> Tuple[str, str]:
        variable_value = varItem["variable_value"]
        variable_shape = varItem["variable_shape"]

        if len(variable_value) > 500:
            target_variable_value = (
                f"array of shape {variable_shape}"
                if variable_shape is not None
                else f"{variable_value[:30]} ... {variable_value[-30:]}"
            )
        else:
            target_variable_value = variable_value

        return target_variable_value, varItem["variable_type"]

    def _resolve_dynamics(self, values):
        iovals = []
        iotypes = []
        for I, O in values:
            ivals = dict()
            itypes = dict()
            cond = Facts._does_this_variable_record_contains_non_empty_value

            for varName, varItem in I.items():
                if cond(varItem):
                    (
                        ivals[varName],
                        itypes[varName],
                    ) = self._resolve_dynamics_value_and_type(varItem)
            ovals = dict()
            otypes = dict()

            for varName, varItem in O.items():
                if cond(varItem):
                    (
                        ovals[varName],
                        otypes[varName],
                    ) = self._resolve_dynamics_value_and_type(varItem)

            # fix issue to have tuple of 2 empty dicts
            if len(ivals.keys()) > 0 or len(ovals.keys()) > 0:
                iovals.append((ivals, ovals))
            if len(itypes.keys()) > 0 or len(otypes.keys()) > 0:
                iotypes.append((itypes, otypes))

        return (iovals, iotypes)

    def _remove_duplicate_io_tuples(self, vvs):
        result = []
        seen = []
        for io_tuple in vvs:
            inv = io_tuple[0]
            if not any(inv == s for s in seen):
                seen.append(inv)
                result.append(io_tuple)
        return result

    def _remove_duplicate_keys(self, vvs):
        result = []
        for i, o in vvs:
            if i and o:  # This checks if both dictionaries are non-empty
                ro = {
                    k: o[k] for k in i if i[k] != o[k]
                }  # Include in 'ro' only if values are different
                result.append((i, ro))
        return result

    def _resolve_angelic_variables(self, function_info):
        if (
            function_info.get("angelic_variable_values") is not None
            and len(function_info["angelic_variable_values"]) > 0
        ):
            # resolve issue: make sure we do not have duplicate inputs
            avv = function_info["angelic_variable_values"]
            avv = self._remove_duplicate_io_tuples(avv)
            avv = self._remove_duplicate_keys(avv)
            ioavals, ioatypes = self._resolve_dynamics(avv)

            # fix issue where angelic and runtime list is empty
            # where they should be empty
            if len(ioavals) > 0:
                self.facts["2.1.5"] = ioavals
            else:
                self._log_stat("angelic_variable_values", (0))
            if len(ioatypes) > 0:
                self.facts["2.1.6"] = ioatypes
            else:
                self._log_stat("angelic_variable_types", (0))

        if (
            function_info.get("variable_values") is not None
            and len(function_info["variable_values"]) > 0
        ):
            # resolve issue: make sure we do not have duplicate inputs
            vv = function_info["variable_values"]
            vv = self._remove_duplicate_io_tuples(vv)
            vv = self._remove_duplicate_keys(vv)
            iobvals, iobtypes = self._resolve_dynamics(vv)

            # fix issue same as above
            if len(iobvals) > 0:
                self.facts["2.1.3"] = iobvals
            else:
                self._log_stat("runtime_variable_values", (0))
            if len(iobtypes) > 0:
                self.facts["2.1.4"] = iobtypes
            else:
                self._log_stat("runtime_variable_types", (0))

    @staticmethod
    def _does_this_2_variable_records_actually_have_changes(
        buggy_variable_record, angelic_variable_record
    ):
        if (
            buggy_variable_record["variable_value"]
            == angelic_variable_record["variable_value"]
            and buggy_variable_record["variable_type"]
            == angelic_variable_record["variable_type"]
        ):
            return False
        return True

    @staticmethod
    def _does_this_variable_record_contains_non_empty_value(variable_record):
        if (
            variable_record["variable_value"] == "None"
            or variable_record["variable_type"] == "None"
            or Facts._matches_builtin_method(variable_record["variable_value"])
        ):
            return False
        return True

    @staticmethod
    def _matches_builtin_method(string):
        pattern = r"<([a-zA-Z\-]+) (?:[^>]+) at 0x[0-9a-f]+>"
        return bool(re.match(pattern, string))

    def _resolve_class_info(self, buggy_class_info):
        class_declearation = buggy_class_info["signature"]
        class_decorators = buggy_class_info["class_decorators"]

        if class_decorators is not None and len(class_decorators) > 0:
            for decorator in class_decorators[::-1]:
                class_declearation = "@" + decorator + "\n" + class_declearation

        self.facts["1.2.1"] = class_declearation

        class_docstring = buggy_class_info["docstring"]
        if class_docstring is not None:
            self.facts["1.2.2"] = class_docstring

        used_methods = []
        method_signatures = buggy_class_info["function_signatures"]
        methods = buggy_class_info["functions"]
        for idx, method in enumerate(methods):
            if self._is_this_func_called(method):
                used_methods.append(method_signatures[idx])
        if len(used_methods) > 0:
            self.facts["1.2.3"] = used_methods

    @staticmethod
    def remove_docstring_from_source(function_source):
        # Regex to match docstrings under a function or method definition
        # The pattern looks for 'def' followed by any characters (non-greedy) up to the first triple quote
        # The re.DOTALL flag allows the dot (.) to match newlines as well
        pattern = r"(def\s.*?:\s*?\n\s*?)\"\"\".*?\"\"\"|\'\'\'.*?\'\'\'"
        return re.sub(pattern, r"\1", function_source, flags=re.DOTALL)

    @staticmethod
    def _split_error_message(error_message) -> List[dict]:
        lines = error_message.split("\n")
        chunks = []
        current_chunk = []
        current_label = ""

        for line in lines:
            # Determine if the line is an error message or stacktrace
            label = "error_message" if line.startswith("E") else "stacktrace"

            # If we are starting a new chunk, add the previous chunk to the list
            if label != current_label and current_chunk:
                record = {"label": current_label, "content": "\n".join(current_chunk)}
                chunks.append(record)
                current_chunk = []

            # Add the line to the current chunk and update the current label
            current_chunk.append(line)
            current_label = label

        # Add the last chunk to the list
        if current_chunk:
            record = {"label": current_label, "content": "\n".join(current_chunk)}
            chunks.append(record)

        return chunks

    def _resolve_test_data(self, test_data):
        test_function_code = test_data["test_function_code"]
        if self.facts["1.4.1"] is None:
            self.facts["1.4.1"] = [test_function_code]
        else:
            self.facts["1.4.1"].append(test_function_code)

        test_file_name = test_data["test_path"]
        if self.facts["1.4.2"] is None:
            self.facts["1.4.2"] = [test_file_name]
        else:
            self.facts["1.4.2"].append(test_file_name)

        full_test_error = test_data["full_test_error"]
        error_stacktrace_chunks = Facts._split_error_message(full_test_error)

        full_stacktrace = []
        full_error_message = []

        is_error_message = None
        for chunk in error_stacktrace_chunks:
            if chunk["label"] == "stacktrace":
                if is_error_message is not None and not is_error_message:
                    raise NotSupportedError("2 error message follow together")
                is_error_message = False
                full_stacktrace.append(chunk["content"])
            elif chunk["label"] == "error_message":
                if is_error_message is not None and is_error_message:
                    raise NotSupportedError("2 stack traces follow together")
                is_error_message = True
                full_error_message.append(chunk["content"])

        if len(full_error_message) > 0:
            if self.facts["2.1.1"] is None:
                self.facts["2.1.1"] = [full_error_message]
            else:
                self.facts["2.1.1"].append(full_error_message)

        if len(full_stacktrace) > 0:
            if self.facts["2.1.2"] is None:
                self.facts["2.1.2"] = [full_stacktrace]
            else:
                self.facts["2.1.2"].append(full_stacktrace)

    @staticmethod
    def _extract_code_blocks_from_markdown(md_content):
        # Regular expression pattern to match code blocks
        # The pattern looks for triple backticks, optionally followed by an identifier (like python, js, etc.)
        # and then any content until the closing triple backticks, across multiple lines
        pattern = r"```[a-zA-Z]*\n(.*?)```"

        # Find all matches in the Markdown content
        matches = re.findall(pattern, md_content, flags=re.DOTALL)

        return matches

    def load_from_bwd(
        self, feature_json_path: str, write_markdown_files=True, write_facts_json=True
    ):
        with open(feature_json_path, "r") as f:
            json_output = json.load(f)

        with open(feature_json_path, "w") as f:
            json.dump(json_output, f, indent=4)

        bugid = self._bugid
        bwd = self._bwd

        self.load_from_json_object(json_output[bugid])

        if write_markdown_files:
            self._write_markdown_files()

        if os.path.exists(os.path.join(bwd, "f3-1-1.md")):
            with open(os.path.join(bwd, "f3-1-1.md"), "r") as f:
                self.facts["3.1.1"] = Facts._extract_code_blocks_from_markdown(f.read())

        if os.path.exists(os.path.join(bwd, "f3-1-2.md")):
            with open(os.path.join(bwd, "f3-1-2.md"), "r") as f:
                self.facts["3.1.2"] = Facts._extract_code_blocks_from_markdown(f.read())

        if write_facts_json:
            # write facts.json file
            with open(os.path.join(bwd, "facts.json"), "w") as f:
                json.dump(self.facts, f, indent=4)

        if self.facts["1.2.3"] is None:
            self._log_stat("method_ref_num_pair", (bugid, 0))
        else:
            self._log_stat("method_ref_num_pair", (bugid, len(self.facts["1.2.3"])))

        if self.facts["1.3.2"] is None:
            self._log_stat("in_scope_func_ref_num_pair", (bugid, 0))
        else:
            self._log_stat(
                "in_scope_func_ref_num_pair", (bugid, len(self.facts["1.3.2"]))
            )

    def _write_markdown_files(self):
        def format_json(obj):
            formatted_json = json.dumps(obj, indent=4)
            return formatted_json

        for fact_key, fact_content in self.facts.items():
            if fact_content is None:
                continue

            fact_name = self.FACT_MAP[fact_key]
            if "code" in fact_name:
                fact_type = "python"
            else:
                fact_type = "text"

            if isinstance(fact_content, list) or isinstance(fact_content, dict):
                fact_content = format_json(fact_content)
                fact_type = "json"
            fact_content = f"```{fact_type}\n{fact_content}\n```\n"

            filename = "f" + fact_key.replace(".", "-") + ".md"
            with open(os.path.join(self._bwd, filename), "w") as f:
                f.write(f"""# {fact_name}\n\n{fact_content}""")

    def report_stats(self) -> str:
        """
        Returns a string containing the statistics of the facts.
        """
        stats = f"LOG: {self._bugid}\n"
        for category, records in self.stats.items():
            stats += f"{category}:\n"
            for record in records:
                stats += f"\t{record}\n"
        return stats


def collect_facts(
    bugid: str,
    bwd: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
):
    if bugid in IGNORED_BUGS:
        print_in_yellow(f"WARNING: {bugid} is ignored")
        return

    if not ensure_clone_and_prep_complete(
        bugid,
        envs_dir,
        use_docker=use_docker,
        overwrite=False,
    ):
        return

    bug_json_file = os.path.join(bwd, "bug-data.json")
    if not run_extract_features_command(
        bugid,
        bug_json_file,
        envs_dir,
        use_docker=use_docker,
        overwrite=overwrite,
    ):
        return

    facts = Facts(bugid, bwd)
    facts.load_from_bwd(bug_json_file, write_markdown_files=True, write_facts_json=True)
    # print_in_yellow(facts.report_stats())
