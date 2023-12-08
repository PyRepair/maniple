import argparse
from doctest import testmod
import json
import subprocess
from typing import List, Literal, Union
from utils import print_in_red
import os


def get_bugids_from_dataset(
    dataset: Union[Literal["106subset"], Literal["395subset"]], test_mode=False
):
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
            "395-dataset.json",
        )

    with open(dataset_indices_file_path, "r") as f:
        dataset_indices = json.load(f)

    bugids = []
    for project_name, bugids_list in dataset_indices.items():
        if test_mode:
            bugids_list = bugids_list[:1]
        for bugid in bugids_list:
            bugids.append(f"{project_name}:{bugid}")

    return bugids


def batch_prepare(bugids: List[str]):
    # assume you have docker built following Nikhil's instructions
    # build instruction see here: https://github.com/PyRepair/PyRepair/tree/master/pyr_benchmark_wrangling

    for bugid in bugids:
        print(f"Cloning {bugid}")
        try:
            output = subprocess.run(
                (
                    f"docker run --rm -it -v /Volumes/SSD2T/envs:/envs "
                    + f"pyr:lite bgp clone --restart --bugids {bugid} --envs-dir /envs"
                ).split(" "),
                capture_output=False,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print_in_red(f"Failed to clone {bugid}")
            with open(f"logs/{bugid}_clone_fail_log.txt", "w") as f:
                f.write(e.stdout.decode("utf-8") + e.stderr.decode("utf-8"))
            continue

        print(f"Preparing {bugid}")
        output = subprocess.run(
            (
                f"docker run --rm -it -v /Volumes/SSD2T/envs:/envs "
                + f"pyr:lite bgp prep --restart --bugids {bugid} --envs-dir /envs"
            ).split(" "),
            capture_output=True,
        )
        all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
        if "TestStatus.PASS" not in all_output:
            print_in_red(f"Failed to prepare {bugid}")
            with open(f"logs/{bugid}_prep_fail_log.txt", "w") as f:
                f.write(all_output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["106subset", "395subset", "all"],
        default="106subset",
        help="Which dataset to prepare",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Whether to run in test mode",
        default=False,
    )
    args = parser.parse_args()

    if args.dataset == "all":
        bugids = get_bugids_from_dataset(
            "106subset", test_mode=args.test_mode
        ) + get_bugids_from_dataset("395subset", test_mode=args.test_mode)
    else:
        bugids = get_bugids_from_dataset(args.dataset, test_mode=args.test_mode)

    batch_prepare(bugids)


if __name__ == "__main__":
    main()
