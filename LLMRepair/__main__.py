import argparse
import os

from utils import print_in_red
from cleaner import clear_features, clear_logs, clear_prompts
from features_extractor import collect_facts, NotSupportedError
from patch_validator import validate_patches
from dataset_manager import load_bugids_from_dataset
from command_runner import ensure_clone_and_prep_complete


def resolve_cli_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "command",
        choices=[
            "prep" "extract",
            "validate",
            "clean_feature_files",
            "clean_log_files",
            "clean_prompt_files",
        ],
        help="specify the command to run",
    )

    group = args_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--bugids",
        type=lambda s: s.split(","),
        help="specify a list of bugids to collect facts, like `pandas:30`",
        default=[],
    )
    group.add_argument(
        "--dataset",
        type=str,
        choices=["106subset", "395subset", "first-stratum", "second-stratum", "all"],
        help="Which dataset to prepare",
        default="all",
    )

    args_parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="specify directory to store prompt and result files",
    )
    args_parser.add_argument(
        "--envs-dir",
        type=str,
        help="specify the path to prepared environments",
        default=None,
    )
    args_parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Take only 1 bug from each project",
        default=False,
    )
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

    if args.database_path is None:
        args_parser.print_help()
        exit(1)

    return args


def main(args):
    if len(args.bugids) > 0:
        bugids = args.bugids
    elif args.dataset == "all":
        s1 = load_bugids_from_dataset("106subset", test_mode=args.test_mode)
        s2 = load_bugids_from_dataset("395subset", test_mode=args.test_mode)
        bugids = s1 + s2
    else:
        bugids = load_bugids_from_dataset(args.dataset, test_mode=args.test_mode)

    for bugid in bugids:
        bwd = os.path.join(args.database_path, *bugid.split(":"))
        if not os.path.exists(bwd):
            os.makedirs(bwd)

        try:
            if args.command == "prep":
                ensure_clone_and_prep_complete(
                    bugid, args.envs_dir, args.use_docker, args.overwrite
                )
            if args.command == "extract":
                collect_facts(
                    bugid, bwd, args.envs_dir, args.use_docker, args.overwrite
                )
            elif args.command == "validate":
                validate_patches(
                    bugid, bwd, args.envs_dir, args.use_docker, args.overwrite
                )
            elif args.command == "clean_feature_files":
                clear_features(bwd)
            elif args.command == "clean_log_files":
                clear_logs(bwd)
            elif args.command == "clean_prompt_files":
                clear_prompts(bwd)

        except NotSupportedError as e:
            print_in_red(f"ERROR: {e}")
            print_in_red(f"Skip {bugid}")


if __name__ == "__main__":
    args = resolve_cli_args()
    main(args)
