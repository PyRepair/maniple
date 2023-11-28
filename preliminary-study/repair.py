import argparse
import os
from extractor import print_in_red, collect_facts, NotSupportedError
from patch_validator import validate_patches


def get_bugids_from_output_dir(output_dir: str):
    dirs = os.listdir(output_dir)
    bugids = []
    for directory in dirs:
        if not os.path.isdir(os.path.join(output_dir, directory)):
            continue
        parts = directory.split("-")
        bugids.append(f"{'-'.join(parts[:-1])}:{parts[-1]}")
    return bugids


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "command",
        choices=["extract_features", "validate_patches"],
        help="specify the command to run"
    )
    args_parser.add_argument(
        "--bugids",
        type=lambda s: s.split(","),
        help="specify a list of bugids to collect facts, like `pandas:30,scikit-learn:1`",
    )
    args_parser.add_argument(
        "-o", "--output-dir", required=True, help="specify the output directory"
    )
    args_parser.add_argument("--overwrite", action="store_true", default=False)
    args = args_parser.parse_args()

    if args.output_dir is None:
        args_parser.print_help()
        exit(1)

    bugids = args.bugids
    if bugids is None:
        bugids = get_bugids_from_output_dir(args.output_dir)

    for bugid in bugids:
        try:
            if args.command == "extract_features":
                collect_facts(bugid, args.output_dir, flag_overwrite=args.overwrite)
            if args.command == "validate_patches":
                validate_patches(bugid, args.output_dir)
        except NotSupportedError as e:
            print_in_red(f"ERROR: {e}")
            print_in_red(f"Skip {bugid}")
