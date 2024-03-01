import argparse
import json
import os
from pathlib import Path
import threading
from typing import List

from maniple.utils.misc import (
    divide_list,
    iter_bugid_folders, 
    print_in_red, 
    print_in_yellow,
    clear_features,
    clear_logs,
    clear_prompts,
    clear_results,
    clear_responses,
)
from maniple.utils.features_extractor import collect_facts, NotSupportedError
from maniple.utils.patch_validator import validate_patches
from maniple.utils.command_runner import ensure_clone_and_prep_complete
from maniple.utils.init_data import init_data


def resolve_cli_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "command",
        choices=[
            "init",
            "prep",
            "extract",
            "validate",
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
        help="Which dataset to prepare",
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

    if args.command in ["init", "validate", "extract"] and args.output_dir is None:
        print_in_red("ERROR: output-dir is required for init, validate and extract")
        exit(-1)
    
    return args


def run_single_partition_bugids(args, bugids: List[str]):
    for bugid in bugids:
        # make sure the output directory exists
        bwd = os.path.join(args.output_dir, *bugid.split(":"))
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
                for bitvector_folder in os.listdir(bwd):
                    bitvector_path = os.path.join(bwd, bitvector_folder)
                    if not os.path.isdir(bitvector_path):
                        continue
                    validate_patches(
                        bugid,
                        bitvector_path,
                        args.envs_dir,
                        args.use_docker,
                        args.overwrite,
                        args.timeout,
                        args.verbose_logging,
                    )

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


def start_multithread_task(args, bugids: List[str]):
    bugids_partitions = divide_list(bugids, args.partitions)

    print(f"Start {args.command} task with {args.partitions} partitions")

    threads = []
    for bugids_partition in bugids_partitions:
        thread = threading.Thread(
            target=run_single_partition_bugids,
            args=(args, bugids_partition),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def start_batch_task(args):
    bugids: List[str] = []
    
    if len(args.bugids) > 0:
        bugids = args.bugids

    elif args.output_dir is not None:
        bugids = [bid for bid, _, _ in iter_bugid_folders(Path(args.output_dir))]

    elif args.dataset is not None:
        _p = Path(__file__).parent.parent / "experiment-initialization-resources" / "datasets-list" / args.dataset
        if not _p.exists():
            print_in_red(f"ERROR: dataset {args.dataset} not found")
            return
        
        with open(_p) as f:
            _j = json.load(f)
            for key, value in _j.items():
                bugids.append(f"{key}:{value}")
    
    else:
        print_in_red("ERROR: no bugids specified")
        return
    
    print(f"Bugids: {bugids}, total: {len(bugids)}")
    start_multithread_task(args, bugids)


def main():
    args = resolve_cli_args()

    if args.command == "init":
        init_data(args.output_dir, args.dataset)
    else:
        start_batch_task(args)
    


if __name__ == "__main__":
    main()
