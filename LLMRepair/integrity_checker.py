import os
import sys
import json
import argparse


def check_for_facts_data(
    path,
    check_source,
    check_error_message,
    check_angelic,
    show_bugids,
    show_stats,
    show_errors,
):
    total_files = 0
    satisfied_files = 0
    bugids = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == "facts.json":
                total_files += 1
                with open(os.path.join(root, file), "r") as f:
                    data = json.load(f)
                    satisfied = True
                    if check_source and (
                        "1.1.1" not in data
                        or data["1.1.1"] is None
                        or data["1.1.1"] == ""
                    ):
                        if show_errors:
                            print(
                                f"The file {file} in the directory {root} does not have buggy code"
                            )
                        satisfied = False
                    if (
                        check_error_message
                        and "2.1.1" not in data
                        and "2.1.2" not in data
                    ):
                        if show_errors:
                            print(
                                f"The file {file} in the directory {root} does not have error messages"
                            )
                        satisfied = False
                    if check_angelic and (
                        "2.1.5" not in data
                        or data["2.1.5"] is None
                        or len(data["2.1.5"]) == 0
                        or all(len(item[1].keys()) == 0 for item in data["2.1.5"])
                    ):
                        if show_errors:
                            print(
                                f"The file {file} in the directory {root} has missing angelic output"
                            )
                        satisfied = False
                    if satisfied:
                        satisfied_files += 1
                        projectname, bugid = root.split(os.sep)[-2:]
                        bugids.append(f"{projectname}:{bugid}")

    if show_stats:
        print(f"Number of files that satisfied the requirements: {satisfied_files}")
        print(
            f"Percentage of files that satisfied the requirements: {int(satisfied_files / total_files * 100)}%"
        )
    if show_bugids:
        print(",".join(bugids))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--check-source", action="store_true")
    parser.add_argument("--check-error-message", action="store_true")
    parser.add_argument("--check-angelic", action="store_true")
    parser.add_argument("--show-bugids", action="store_true")
    parser.add_argument("--show-stats", action="store_true")
    parser.add_argument("--show-errors", action="store_true")
    args = parser.parse_args()

    check_for_facts_data(
        args.path,
        args.check_source,
        args.check_error_message,
        args.check_angelic,
        args.show_bugids,
        args.show_stats,
        args.show_errors,
    )
