import argparse
import json
import subprocess
from typing import List, Literal, Union
from utils import print_in_red, print_in_yellow
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


def run_clone_command(
    bugid: str, dest_env: str, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")
    repo_dir = os.path.join(dest_env, "repos", path_bugid_name)
    if not overwrite and os.path.exists(repo_dir):
        print_in_yellow(f"Skipping cloning {bugid} because it already exists")
        return False

    print(f"Cloning {bugid}")

    try:
        if use_docker:
            subprocess.run(
                (
                    f"docker run --rm -it -v {dest_env}:/envs pyr:lite "
                    + f"bgp clone --restart --bugids {bugid} --envs-dir /envs"
                ).split(" "),
                capture_output=True,
                check=True,
            )
        else:
            cmd = f"bgp clone --restart --bugids {bugid} --envs-dir {dest_env}"
            subprocess.run(
                cmd.split(" "),
                capture_output=True,
                check=True,
            )

    except subprocess.CalledProcessError as e:
        print_in_red(f"Failed to clone {bugid}")
        with open(f"logs/{path_bugid_name}_clone_fail_log.txt", "w") as f:
            f.write(e.stdout.decode("utf-8") + e.stderr.decode("utf-8"))
        return False

    return True


def run_prepare_command(
    bugid: str, dest_env: str, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")
    env_dir = os.path.join(dest_env, "envs", path_bugid_name)
    if not overwrite and os.path.exists(env_dir):
        print_in_yellow(f"Skipping preparing {bugid} because it already exists")
        return False

    print(f"Preparing {bugid}")

    if use_docker:
        output = subprocess.run(
            (
                f"docker run --rm -it -v {dest_env}:/envs "
                + f"pyr:lite bgp prep --restart --bugids {bugid} --envs-dir /envs"
            ).split(" "),
            capture_output=True,
        )
    else:
        output = subprocess.run(
            (f"bgp prep --restart --bugids {bugid} --envs-dir {dest_env}").split(" "),
            capture_output=True,
        )

    all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
    if "TestStatus.PASS" not in all_output:
        print_in_red(f"Failed to prepare {bugid}")
        with open(f"logs/{path_bugid_name}_prep_fail_log.txt", "w") as f:
            f.write(all_output)
        return False

    return True


def batch_prepare(bugids: List[str], dest_env: str, overwrite=False, use_docker=False):
    # assume you have docker built following Nikhil's instructions
    # build instruction see here: https://github.com/PyRepair/PyRepair/tree/master/pyr_benchmark_wrangling

    for bugid in bugids:
        clone_result = run_clone_command(
            bugid, dest_env, use_docker=use_docker, overwrite=overwrite
        )
        if not clone_result:
            continue

        run_prepare_command(bugid, dest_env, use_docker=use_docker, overwrite=overwrite)


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
        bugids, args.envs_dir, overwrite=args.overwrite, use_docker=args.use_docker
    )


if __name__ == "__main__":
    main()
