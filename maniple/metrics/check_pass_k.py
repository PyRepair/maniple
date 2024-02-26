import argparse
from collections import defaultdict
from pathlib import Path
import json
from typing import List
import numpy as np

from maniple.utils.misc import iter_bugid_folders


def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0

    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def analyze(folder: List[Path]):
    fixes_per_bug = defaultdict[str, int](lambda: 0) # all 1 bitvector
    trials_per_bug = defaultdict[str, int](lambda: 0) # all 1 bitvector

    total_fixes_per_bug = defaultdict[str, int](lambda: 0)
    total_trials_per_bug = defaultdict[str, int](lambda: 0)

    lst = []
    for f in folder:
        _lst = iter_bugid_folders(f)
        lst.extend(_lst)
    
    for bugid, project_folder, bugid_folder in lst:
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
                with open(file, "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                if first_value == 0:
                    fixes_per_bug[bugid] += 1
                
                if first_value == 0 or first_value == 1:
                    trials_per_bug[bugid] += 1
            
            if "result" in file.name and file.name.endswith(".json"):
                with open(file, "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                if first_value == 0:
                    total_fixes_per_bug[bugid] += 1
                
                if first_value == 0 or first_value == 1:
                    total_trials_per_bug[bugid] += 1

    return fixes_per_bug, trials_per_bug, total_fixes_per_bug, total_trials_per_bug


def print_result(trials_per_bug, fixes_per_bug, benchmark_trials_per_bug=None, benchmark_fixes_per_bug=None):
    pass_k_sum = [0.0] * 10
    benchmark_pass_k_sum = [0.0] * 10

    for _bugid in trials_per_bug.keys():
        fixes_count = fixes_per_bug[_bugid]
        trials_count = trials_per_bug[_bugid]

        if benchmark_trials_per_bug is not None and benchmark_fixes_per_bug is not None:
            if benchmark_trials_per_bug[_bugid] == 0:
                print("nothing to compare")
            else:
                print(
                    f"Bug {_bugid} current: {fixes_count}/{trials_per_bug[_bugid]} benchmark: {benchmark_fixes_per_bug[_bugid]}/{benchmark_trials_per_bug[_bugid]}"
                )
        else:
            print(f"Bug {_bugid} {fixes_count}/{trials_per_bug[_bugid]}")

        for k in range(1, 11):
            pass_k_sum[k - 1] += pass_at_k(trials_count, fixes_count, k)
            if benchmark_trials_per_bug is not None and benchmark_fixes_per_bug is not None:
                benchmark_pass_k_sum[k - 1] += pass_at_k(benchmark_trials_per_bug[_bugid], benchmark_fixes_per_bug[_bugid], k)

    for k in range(1, 11):
        if benchmark_trials_per_bug is not None and benchmark_fixes_per_bug is not None:
            print(f"pass@{k} current: {pass_k_sum[k - 1] / len(fixes_per_bug.keys())} benchmark: {benchmark_pass_k_sum[k - 1] / len(fixes_per_bug.keys())}")
        else:
            print(f"pass@{k} {pass_k_sum[k - 1] / len(fixes_per_bug.keys())}")


def check_pass_k(current_path: List[Path], benchmark_path: List[Path] | None = None, show_full_bitvector=False):
    if benchmark_path is None:
        fixes_per_bug, trials_per_bug, total_fixes_per_bug, total_trials_per_bug = analyze(current_path)

        if show_full_bitvector:
            print("All 1 bitvector")
            print_result(trials_per_bug, fixes_per_bug)
            print()

        print("All bitvectors")
        print_result(total_trials_per_bug, total_fixes_per_bug)
        
    else:
        fixes_per_bug, trials_per_bug, total_fixes_per_bug, total_trials_per_bug = analyze(current_path)
        benchmark_fixes_per_bug, benchmark_trials_per_bug, benchmark_total_fixes_per_bug, benchmark_total_trials_per_bug = analyze(benchmark_path)

        if show_full_bitvector:
            print("All 1 bitvector")
            print_result(trials_per_bug, fixes_per_bug, benchmark_trials_per_bug, benchmark_fixes_per_bug)
            print()

        print("All bitvectors")
        print_result(total_trials_per_bug, total_fixes_per_bug, benchmark_total_trials_per_bug, benchmark_total_fixes_per_bug)


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("current_path", type=lambda x: [Path(p) for p in x.split(",")])
    args_parser.add_argument("--benchmark-path", type=lambda x: [Path(p) for p in x.split(",")], required=False, default=None)
    args_parser.add_argument("--show-full-bitvector", action="store_true", required=False)
    
    args = args_parser.parse_args()

    check_pass_k(args.current_path, args.benchmark_path, args.show_full_bitvector)


if __name__ == "__main__":
    main()
