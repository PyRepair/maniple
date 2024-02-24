import argparse
import os
import shutil
import threading
from typing import List

from utils import (
    divide_list, 
    print_in_red, 
    print_in_yellow,
    clear_features,
    clear_logs,
    clear_prompts,
    clear_results,
    clear_responses,
)
from features_extractor import collect_facts, NotSupportedError
from patch_validator import validate_patches
from dataset_manager import load_bugids_from_dataset, split_bugids_from_dataset
from command_runner import ensure_clone_and_prep_complete


def resolve_cli_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "command",
        choices=[
            "prep",
            "extract",
            "validate",
            "copy",
            "clean_feature_files",
            "clean_response_files",
            "clean_result_files",
            "clean_log_files",
            "clean_prompt_files",
        ],
        help="specify the command to run",
    )

    group_resource = args_parser.add_mutually_exclusive_group()
    group_resource.add_argument(
        "--bugids",
        type=lambda s: s.split(","),
        help="specify a list of bugids to collect facts, like `pandas:30`",
        default=[],
    )
    group_resource.add_argument(
        "--dataset",
        type=str,
        choices=[
            "BGP100",
            "BGP215",
            "first-stratum",
            "second-stratum",
            "all",
        ],
        help="Which dataset to prepare",
        default="all",
    )
    group_resource.add_argument(
        "--use-bugs-directory",
        type=str,
        help="load bugids from specified directory",
        default=None,
    )

    group_include_exclude = args_parser.add_mutually_exclusive_group()
    group_include_exclude.add_argument(
        "--exclude-projects",
        type=lambda s: s.split(","),
        help="specify a list of projects to exclude",
        default=[],
    )
    group_include_exclude.add_argument(
        "--include-projects",
        type=lambda s: s.split(","),
        help="specify a list of projects to include",
        default=[],
    )

    args_parser.add_argument(
        "--output-dir",
        type=str,
        help="configure the output directory to save prompt and result files. This setup is useful for redirecting outputs from validation processes or fact extraction results. Additionally, it allows for specifying target locations when using the copy command.",
        required=False,
        default=None,
    )

    args_parser.add_argument(
        "--verbose-logging",
        action="store_true",
        help="whether print verbose logging",
        default=False,
    )

    args_parser.add_argument(
        "--timeout",
        type=int,
        help="specify the timeout in seconds",
        default=30,
    )

    # Update 8th Jan, 2024: Since multiprocessing tends to be stable and well tested right now
    # use 4 as a optimal number to leverage computing resources.
    args_parser.add_argument(
        "--partitions",
        type=int,
        help="specify the number of partitions",
        default=4,
    )

    args_parser.add_argument(
        "--envs-dir",
        type=str,
        help="specify the path to prepared environments",
        default=None,
    )

    # --use-supported flag is deprecated on 8th Jan, 2024 since supported project list is confirmed now.
    # args_parser.add_argument(
    #     "--use-supported",
    #     action="store_true",
    #     help="Take only supported projects",
    #     default=False,
    # )

    args_parser.add_argument(
        "--overwrite",
        help="whether overwrite existing results",
        action="store_true",
        default=False,
    )

    args_parser.add_argument(
        "--use-docker",
        help="whether use docker to run the command",
        action="store_true",
        default=False,
    )

    args = args_parser.parse_args()

    return args


def copy_bugids(bugids: List[str], source_dir: str, dest_dir: str):
    for bugid in bugids:
        dest_path = os.path.join(dest_dir, *bugid.split(":"))
        os.makedirs(dest_path, exist_ok=True)
        shutil.copytree(source_dir, dest_path, dirs_exist_ok=True)


def run_single_partition_bugids(args, bugids: List[str], source_dir: str):
    for bugid in bugids:
        # if we are not copying files, we are allowed to switch destination directory
        if args.output_dir is not None and args.command != "copy":
            source_dir = args.output_dir

        # if destination directory is specified, make sure it exists
        if args.output_dir is not None and not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        # make sure the working directory exists
        bwd = os.path.join(source_dir, *bugid.split(":"))
        if not os.path.exists(bwd):
            os.makedirs(bwd)

        try:
            if args.command == "prep":
                ensure_clone_and_prep_complete(
                    bugid,
                    args.envs_dir,
                    args.use_docker,
                    args.overwrite,
                    args.verbose_logging,
                )

            elif args.command == "extract":
                collect_facts(
                    bugid,
                    bwd,
                    args.envs_dir,
                    args.use_docker,
                    args.overwrite,
                    args.verbose_logging,
                )

            elif args.command == "validate":
                validate_patches(
                    bugid,
                    bwd,
                    args.envs_dir,
                    args.use_docker,
                    args.overwrite,
                    args.timeout,
                    args.verbose_logging,
                )

            elif args.command == "copy":
                if args.output_dir is None:
                    print_in_red("FATAL: output_dir not specified")
                    exit(-1)
                copy_bugids(bugids, bwd, args.output_dir)

            elif args.command == "clean_feature_files":
                clear_features(bwd)
            elif args.command == "clean_log_files":
                clear_logs(bwd)
            elif args.command == "clean_prompt_files":
                clear_prompts(bwd)
            elif args.command == "clean_result_files":
                clear_results(bwd)
            elif args.command == "clean_response_files":
                clear_responses(bwd)

        except NotSupportedError as e:
            print_in_yellow(f"WARNING: {e}, skip bugid: {bugid}")


def start_multithread_task(args, bugids: List[str], source_dir: str):
    bugids_partitions = divide_list(bugids, args.partitions)

    threads = []
    for bugids_partition in bugids_partitions:
        thread = threading.Thread(
            target=run_single_partition_bugids,
            args=(args, bugids_partition, source_dir),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main(args):
    if len(args.bugids) > 0:
        bugids = split_bugids_from_dataset(
            args.bugids,
            exclude_projects=args.exclude_projects,
            include_projects=args.include_projects,
        )

    elif args.use_bugs_directory is not None:
        # load bugids from specified directory
        src_dir = args.use_bugs_directory

        # build bugids list by traversing the directory
        bugids_list = []
        for project_name in os.listdir(src_dir):
            project_path = os.path.join(src_dir, project_name)
            if not os.path.isdir(project_path):
                continue
            for bugid in os.listdir(project_path):
                bug_path = os.path.join(project_path, bugid)
                if not os.path.isdir(bug_path):
                    continue
                bugids_list.append(f"{project_name}:{bugid}")

        bugids = split_bugids_from_dataset(
            bugids_list,
            exclude_projects=args.exclude_projects,
            include_projects=args.include_projects,
        )

    else:
        bugids = load_bugids_from_dataset(
            args.dataset,
            exclude_projects=args.exclude_projects,
            include_projects=args.include_projects,
        )

    for source_dir, bugids in bugids:
        if len(bugids) == 0:
            continue

        print(
            f"Output directory: {source_dir if args.output_dir is None else args.output_dir}"
        )
        print(f"Bugids: {bugids}, total: {len(bugids)}")
        start_multithread_task(args, bugids, source_dir)


if __name__ == "__main__":
    args = resolve_cli_args()
    main(args)
