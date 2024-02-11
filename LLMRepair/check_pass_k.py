import argparse
from collections import OrderedDict, defaultdict
from pathlib import Path
from dataclasses import dataclass, field, fields
from utils import iter_bugid_folders
import os
import json
from typing import Dict, List, Set
import numpy as np


def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0

    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def all_one_bitvector_bench():
    fixes_per_bug = defaultdict[str, int](lambda: 0)
    trials_per_bug = defaultdict[str, int](lambda: 0)
    folder = "/Users/jerry/Documents/GitHub/LPPR/test-data/bench"
    for bugid, project_folder, bugid_folder in iter_bugid_folders(Path(folder)):
        max_len = 0
        max_bitvector = ""
        for file in bugid_folder.iterdir():
            if "response" in file.name and file.name.endswith(".json"):
                bitvector = file.name.split("_")[0]
                i = 0
                for bit in bitvector:
                    if bit == "1":
                        i += 1
                if i > max_len:
                    max_len = i
                    max_bitvector = bitvector

        for file in bugid_folder.iterdir():
            if "result" in file.name and max_bitvector in file.name and file.name.endswith(".json"):
                trials_per_bug[bugid] += 1
                with open(file, "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                if first_value == 0:
                    fixes_per_bug[bugid] += 1

    print("All one bitvector bench")
    pass_k_sum = [0.0] * 10

    for _bugid in trials_per_bug.keys():
        fixes_count = fixes_per_bug[_bugid]
        trials_count = trials_per_bug[_bugid]

        print(
            f"Bug {_bugid} has {fixes_count} fixes out of {trials_per_bug[_bugid]} trials"
        )

        for k in range(1, 11):
            pass_k_sum[k - 1] += pass_at_k(trials_count, fixes_count, k)

    for k in range(1, 11):
        print(f"pass@{k}: {pass_k_sum[k - 1] / len(fixes_per_bug.keys())}")


def main(path: str):
    fixes_per_bug = defaultdict[str, int](lambda: 0)
    trials_per_bug = defaultdict[str, int](lambda: 0)

    for root, _, files in os.walk(path):
        parts = root.strip(os.sep).split(os.sep)
        bugid = ":".join(parts[-2:])

        for file in files:
            if "result" in file and file.endswith(".json"):
                result_file_path = os.path.join(root, file)
                with open(result_file_path, "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                trials_per_bug[bugid] += 1

                if first_value == 0:
                    fixes_per_bug[bugid] += 1

    pass_k_sum = [0.0] * 10

    for _bugid in trials_per_bug.keys():
        fixes_count = fixes_per_bug[_bugid]
        trials_count = trials_per_bug[_bugid]

        print(
            f"Bug {_bugid} has {fixes_count} fixes out of {trials_per_bug[_bugid]} trials"
        )

        for k in range(1, 11):
            pass_k_sum[k - 1] += pass_at_k(trials_count, fixes_count, k)

    for k in range(1, 11):
        print(f"pass@{k}: {pass_k_sum[k - 1] / len(fixes_per_bug.keys())}")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("path", help="Path to be taken")
    
    args = args_parser.parse_args()

    main(args.path)
    all_one_bitvector_bench()
