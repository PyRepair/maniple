import argparse
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field, fields
import os
import json
from typing import Dict, List, Set


@dataclass
class PassStats:
    # prompt wise
    count_0: int = 0
    count_0_result_labels: set = field(default_factory=set)

    count_1: int = 0
    count_2: int = 0
    count_4: int = 0
    count_6_7: int = 0
    count_other: int = 0

    # used to track the progress of validation
    total_results: int = 0
    total_results_set: set = field(default_factory=set)
    total_responses: int = 0
    total_responses_set: set = field(default_factory=set)

    fixed_bugids: set = field(default_factory=set)


@dataclass
class ErrorStats:
    flag_2: List[str] = field(default_factory=list)
    flag_4: List[str] = field(default_factory=list)


def print_top10_bitvectors_for_each_bug(allPassStats: OrderedDict[int, PassStats]):
    top_bitvectors_foreach_bug = defaultdict[str, Dict[str, int]](dict)

    for _, passItem in allPassStats.items():
        for result_label in passItem.count_0_result_labels:
            bugid, bitvector = result_label.split("_")
            top_bitvectors_foreach_bug[bugid][bitvector] = (
                top_bitvectors_foreach_bug[bugid].get(bitvector, 0) + 1
            )

    for bugid, bitvector_count in top_bitvectors_foreach_bug.items():
        sorted_bitvector_count = sorted(
            bitvector_count.items(), key=lambda item: item[1], reverse=True
        )
        print(f"bugid: {bugid}")
        for bitvector, count in sorted_bitvector_count[:10]:
            print(f"{bitvector}: {count}")
        print()


def print_top5_bitvectors_and_fix_rate(allPassStats: OrderedDict[int, PassStats]):
    top_fixed_bugids_for_each_bitvector = defaultdict[str, Set[str]](set)

    for _, passItem in allPassStats.items():
        for result_label in passItem.count_0_result_labels:
            bugid, bitvector = result_label.split("_")
            top_fixed_bugids_for_each_bitvector[bitvector].add(bugid)

    top5_ordered_top_fixed_bugids_for_each_bitvector = OrderedDict(
        list(
            sorted(
                top_fixed_bugids_for_each_bitvector.items(),
                key=lambda item: len(item[1]),
                reverse=True,
            )
        )[:5]
    )

    for (
        bitvector,
        fixed_bugids,
    ) in top5_ordered_top_fixed_bugids_for_each_bitvector.items():
        print(f"bitvector: {bitvector}")
        print(f"Number of fixed bugs: {len(fixed_bugids)}")
        print(f"Fix rate: {len(fixed_bugids) / len(allPassStats)}")
        print()


def aggregate_stats(pass_stats_list: Dict[int, PassStats]):
    # Separate fields into integer fields and set fields
    int_fields = [
        f.name
        for f in fields(PassStats)
        if isinstance(getattr(PassStats, f.name, None), int)
    ]
    set_fields = [
        f.name
        for f in fields(PassStats)
        if isinstance(getattr(PassStats, f.name, None), set)
    ]

    # Initialize aggregate values for integer fields
    agg_int_values = {field: 0 for field in int_fields}
    # Initialize empty sets for set fields
    agg_set_values = {field: set() for field in set_fields}

    # Aggregate values for each PassStats object in the list
    for _, stats in pass_stats_list.items():
        for field in int_fields:
            agg_int_values[field] += getattr(stats, field)
        for field in set_fields:
            agg_set_values[field] |= getattr(stats, field)  # Union operation

    # Exclude 'pass_num' from aggregation and set it to a specific value
    agg_int_values.pop("pass_num", None)

    # Create a new PassStats object with aggregated values
    aggregated_values = {**agg_int_values, **agg_set_values}
    return PassStats(**aggregated_values)


def check(path: str, top=None, verbose=None):
    # A dictionary of pass index to PassStats
    allPassStats = defaultdict[int, PassStats](PassStats)

    # A dictionary of bugid to ErrorStats
    bugs_error_stats = defaultdict[str, ErrorStats](ErrorStats)

    fixed_bugids = set()
    postive_labels = set()
    total_bugs = 0

    for root, _, files in os.walk(path):
        bug_fixed_in_folder = False
        parts = root.strip(os.sep).split(os.sep)
        bugid = ":".join(parts[-2:])

        for file in files:
            if "facts.json" == file:
                total_bugs += 1

            if "response" in file and file.endswith(".json"):
                just_filename_parts = file[:-5].split("_")
                pass_index = int(just_filename_parts[-1])
                if top is not None and pass_index > top:
                    continue

                bitvector = just_filename_parts[0]
                result_label = f"{bugid}_{bitvector}"

                allPassStats[pass_index].total_responses_set.add(result_label)
                allPassStats[pass_index].total_responses += 1

            if "result" in file and file.endswith(".json"):
                just_filename_parts = file[:-5].split("_")
                pass_index = int(just_filename_parts[-1])
                if top is not None and pass_index > top:
                    continue

                bitvector = just_filename_parts[0]
                result_label = f"{bugid}_{bitvector}"

                allPassStats[pass_index].total_results_set.add(result_label)
                allPassStats[pass_index].total_results += 1

                result_file_path = os.path.join(root, file)
                with open(result_file_path, "r") as json_file:
                    result_data = json.load(json_file)

                first_key = list(result_data.keys())[0]
                first_value = result_data[first_key]

                if first_value == 0:
                    allPassStats[pass_index].count_0 += 1

                    # for initial results
                    postive_labels.add(result_label)

                    # for each passes, for deduplicated results
                    allPassStats[pass_index].count_0_result_labels.add(result_label)

                    # for each passes, for deduplicated fixed bugids
                    allPassStats[pass_index].fixed_bugids.add(bugid)

                    # set the state of the bug to fixed
                    bug_fixed_in_folder = True

                elif first_value == 1:
                    allPassStats[pass_index].count_1 += 1

                elif first_value == 2:
                    allPassStats[pass_index].count_2 += 1
                    bugs_error_stats[bugid].flag_2.append(result_file_path)

                elif first_value == 4:
                    allPassStats[pass_index].count_4 += 1
                    bugs_error_stats[bugid].flag_4.append(result_file_path)

                elif first_value == 6 or first_value == 7:
                    allPassStats[pass_index].count_6_7 += 1

                else:
                    allPassStats[pass_index].count_other += 1

        if bug_fixed_in_folder:
            fixed_bugids.add(bugid)

    allPassStats = OrderedDict(sorted(allPassStats.items()))
    aggregated_stats: PassStats = aggregate_stats(allPassStats)

    print(
        f"Progress: {int((aggregated_stats.total_results / aggregated_stats.total_responses) * 100)}% Files: {aggregated_stats.total_results}/{aggregated_stats.total_responses}"
    )
    print(
        f"Number of bugs fixed: {len(fixed_bugids)} out of {total_bugs}, percentage: {int((len(fixed_bugids) / total_bugs) * 100)}%"
    )
    print(f"Number of positive labels: {len(postive_labels)} (deduplicated)")
    print(f"Number of positive labels: {aggregated_stats.count_0}")

    # print_top10_bitvectors_for_each_bug(allPassStats)

    # print_top5_bitvectors_and_fix_rate(allPassStats)
    
    if not verbose:
        return
    
    accumulated_fixed_bugids = set()
    accumulated_postive_labels = set()

    for idx, pass_stat in allPassStats.items():
        print()
        print(f"Pass #{idx}")
        print(
            f"Number of bugs fixed: {len(pass_stat.fixed_bugids)} out of {total_bugs}, percentage: {int((len(pass_stat.fixed_bugids) / total_bugs) * 100)}%"
        )
        accumulated_fixed_bugids |= pass_stat.fixed_bugids
        print(
            f"Number of bugs fixed (accumulated): {len(accumulated_fixed_bugids)} out of {total_bugs}, percentage: {int((len(accumulated_fixed_bugids) / total_bugs) * 100)}%"
        )

        print(
            f"Number of postive labels (flag 0): {pass_stat.count_0}, percentage: {int((pass_stat.count_0 / pass_stat.total_results) * 100)}%"
        )
        accumulated_postive_labels |= pass_stat.count_0_result_labels
        print(
            f"Number of postive labels (accumulated): {len(accumulated_postive_labels)} out of {pass_stat.total_results}, percentage: {int((len(accumulated_postive_labels) / pass_stat.total_results) * 100)}%"
        )

        print(
            f"Number of fail labels (flag 1): {pass_stat.count_1}, percentage: {int((pass_stat.count_1 / pass_stat.total_results) * 100)}%"
        )
        print(
            f"Number of test running timeouts (flag 2): {pass_stat.count_2}, percentage: {int((pass_stat.count_2 / pass_stat.total_results) * 100)}%"
        )
        print(
            f"Number of test running errors (flag 4): {pass_stat.count_4}, percentage: {int((pass_stat.count_4 / pass_stat.total_results) * 100)}%"
        )
        print(
            f"Number of bugs that cannot extract functions (flag 6 or 7): {pass_stat.count_6_7}, percentage: {int((pass_stat.count_6_7 / pass_stat.total_results) * 100)}%"
        )
        print(
            f"Number of other errors: {pass_stat.count_other}, percentage: {int((pass_stat.count_other / pass_stat.total_results) * 100)}%"
        )

    print()
    print("Top 5 errornous bugs (flag 2)")
    sorted_bugs_error_stats = sorted(
        bugs_error_stats.items(),
        key=lambda item: len(item[1].flag_2),
        reverse=True,
    )
    for bugid, error_stats in sorted_bugs_error_stats[:5]:
        print(f"bugid: {bugid}")
        print(f"Flag 2: {len(error_stats.flag_2)}")
        for error_filename in error_stats.flag_2:
            print(error_filename)
        print()

    print()
    print("Top 5 errornous bugs (flag 4)")
    sorted_bugs_error_stats = sorted(
        bugs_error_stats.items(),
        key=lambda item: len(item[1].flag_4),
        reverse=True,
    )
    for bugid, error_stats in sorted_bugs_error_stats[:5]:
        print(f"bugid: {bugid}")
        print(f"Flag 4: {len(error_stats.flag_4)}")
        for error_filename in error_stats.flag_4:
            print(error_filename)
        print()


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("path", help="Path to be taken")
    args_parser.add_argument(
        "--top", help="Top number of passed to be printed", type=int, default=None
    )
    args_parser.add_argument(
        "--verbose", help="Print verbose information", action="store_true", default=None
    )

    args = args_parser.parse_args()
    check(args.path, args.top, args.verbose)


if __name__ == "__main__":
    main()
