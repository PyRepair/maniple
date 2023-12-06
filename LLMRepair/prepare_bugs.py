import argparse
import json
import subprocess
from typing import List, Literal, Union
from utils import print_in_red
import os


def get_bugids_from_dataset(dataset: Union[Literal["106subset"], Literal["396subset"]]):
    current_script_path = os.path.dirname(os.path.abspath(__file__))

    if dataset == "106subset":
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "106-dataset.json",
        )
    else:
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "396-dataset.json",
        )

    with open(dataset_indices_file_path, "r") as f:
        dataset_indices = json.load(f)

    bugids = []
    for project_name, bugids_list in dataset_indices.items():
        for bugid in bugids_list:
            bugids.append(f"{project_name}:{bugid}")

    return bugids


def batch_prepare(bugids: List[str]):
    # assume you have docker built following Nikhil's instructions
    # build instruction see here: https://github.com/PyRepair/PyRepair/tree/master/pyr_benchmark_wrangling

    for bugid in bugids:
        print(f"Preparing {bugid}")
        commands = (
            "docker run --rm -it -v /Volumes/JerrySSD/envs:/envs "
            + f"pyr:lite bgp prep --bugids {bugid} --reinstall --separate-envs "
            + "--envs-dir /envs"
        )
        commands = commands.split(" ")
        output = subprocess.run(
            commands,
            capture_output=True,
        )
        all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
        if "TestStatus.PASS" not in all_output:
            print_in_red(f"Failed to prepare {bugid}")
            with open(f"{bugid}_fail_log.txt", "w") as f:
                f.write(all_output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["106subset", "396subset"],
        default="106subset",
        help="Which dataset to prepare",
    )
    args = parser.parse_args()
    bugids = get_bugids_from_dataset(args.dataset)
    batch_prepare(bugids)


if __name__ == "__main__":
    main()
