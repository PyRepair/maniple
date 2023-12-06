import argparse
import os
from utils import print_in_red
from cleaner import clear_features, clear_logs, clear_prompts
from features_extractor import collect_facts, NotSupportedError
from patch_validator import validate_patches


def get_bugids_from_database_path(database_path: str):
    dirs = os.listdir(database_path)
    bugids = []
    for directory in dirs:
        if not os.path.isdir(os.path.join(database_path, directory)):
            continue
        parts = directory.split("-")
        bugids.append(f"{'-'.join(parts[:-1])}:{parts[-1]}")
    return bugids


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "command",
        choices=[
            "extract_features",
            "validate_patches",
            "clean_feature_files",
            "clean_log_files",
            "clean_prompt_files",
        ],
        help="specify the command to run",
    )
    args_parser.add_argument(
        "--bugids",
        type=lambda s: s.split(","),
        help="specify a list of bugids to collect facts, like `pandas:30,scikit-learn:1`",
    )
    args_parser.add_argument(
        "-p",
        "--database-path",
        type=str,
        required=True,
        help="specify the path to bug database",
    )
    args_parser.add_argument(
        "--overwrite",
        help="whether overwrite existing results",
        action="store_true",
        default=False,
    )
    args = args_parser.parse_args()

    if args.database_path is None:
        args_parser.print_help()
        exit(1)

    bugids = args.bugids
    if bugids is None:
        bugids = get_bugids_from_database_path(args.database_path)

    flag_overwrite = args.overwrite

    for bugid in bugids:
        bwd = os.path.join(args.database_path, "-".join(bugid.split(":")))
        if not os.path.exists(bwd):
            os.makedirs(bwd)

        try:
            if args.command == "extract_features":
                collect_facts(bugid, bwd, flag_overwrite)
            elif args.command == "validate_patches":
                validate_patches(bugid, bwd, flag_overwrite)
            elif args.command == "clean_feature_files":
                clear_features(bwd)
            elif args.command == "clean_log_files":
                clear_logs(bwd)
            elif args.command == "clean_prompt_files":
                clear_prompts(bwd)

        except NotSupportedError as e:
            print_in_red(f"ERROR: {e}")
            print_in_red(f"Skip {bugid}")
