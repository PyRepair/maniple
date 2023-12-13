import argparse
import os
import json


def main(path):
    count_1, count_0, count_4, count_other, total, bugs_fixed, total_bugs = (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )

    for root, _, files in os.walk(path):
        bug_fixed_in_folder = False

        for file in files:
            if "facts.json" == file:
                total_bugs += 1

            if "result" in file and file.endswith(".json"):
                total += 1

                with open(os.path.join(root, file), "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                if first_value == 1:
                    count_1 += 1
                elif first_value == 0:
                    count_0 += 1
                    bug_fixed_in_folder = True
                elif first_value == 4:
                    count_4 += 1
                else:
                    count_other += 1

        if bug_fixed_in_folder:
            bugs_fixed += 1

    print(
        f"Number of bugs fixed: {bugs_fixed} out of {total_bugs}, percentage: {int((bugs_fixed / total_bugs) * 100)}%"
    )
    print(
        f"Number of postive labels (flag 0): {count_0}, percentage: {int((count_0 / total) * 100)}%"
    )
    print(
        f"Number of fail labels (flag 1): {count_1}, percentage: {int((count_1 / total) * 100)}%"
    )
    print(
        f"Number of test running errors (flag 4): {count_4}, percentage: {int((count_4 / total) * 100)}%"
    )
    print(
        f"Number of other errors: {count_other}, percentage: {int((count_other / total) * 100)}%"
    )


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("path", help="Path to be taken")

    args = args_parser.parse_args()
    main(args.path)
