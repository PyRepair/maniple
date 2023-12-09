import argparse
import json
from typing import List, Literal, Union
import os

from command_runner import ensure_clone_and_prep_complete


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


def batch_prepare(bugids: List[str], envs_dir: str, use_docker=False, overwrite=False):
    # assume you have docker built following Nikhil's instructions
    # build instruction see here: https://github.com/PyRepair/PyRepair/tree/master/pyr_benchmark_wrangling

    for bugid in bugids:
        ensure_clone_and_prep_complete(bugid, envs_dir, use_docker, overwrite)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        choices=["106subset", "395subset", "all"],
        required=False,
        help="Which dataset to prepare",
    )
    parser.add_argument(
        "--bugids",
        type=lambda s: [item for item in s.split(",")],
        required=False,
        help="Which bugids to prepare",
        default=[],
    )
    parser.add_argument(
        "--envs-dir",
        type=str,
        required=True,
        help="Where to store the prepared environments",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Whether to run in test mode",
        default=False,
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Whether to overwrite existing data",
        default=False,
    )
    parser.add_argument(
        "--use-docker",
        action="store_true",
        help="Whether to use docker",
        default=False,
    )
    args = parser.parse_args()

    if len(args.bugids) > 0:
        bugids = args.bugids
    elif args.dataset == "all":
        bugids = get_bugids_from_dataset(
            "106subset", test_mode=args.test_mode
        ) + get_bugids_from_dataset("395subset", test_mode=args.test_mode)
    else:
        bugids = get_bugids_from_dataset(args.dataset, test_mode=args.test_mode)

    batch_prepare(
        bugids,
        args.envs_dir,
        use_docker=args.use_docker,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
