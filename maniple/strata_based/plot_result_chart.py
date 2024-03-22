import json
import os.path
from itertools import combinations

import pandas as pd
import upsetplot
from pandas import DataFrame
from upsetplot import UpSet, from_contents
from collections import Counter
from matplotlib import pyplot as plt
from upsetplot import plot


def create_raw_bitvector_fix_rate(test_data, filename):
    test_data['bitvector'] = test_data.iloc[:, 2:9].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
    # Group by the 'bitvector' and count the values in column 19
    grouped_by_bitvector = test_data.groupby(['bitvector', test_data.columns[9]]).size().unstack(fill_value=0)
    # Reset index to make 'bitvector' a column
    bitvector_raw_fix_rate = grouped_by_bitvector.reset_index()
    bitvector_raw_fix_rate.to_excel(os.path.join(result_sheet_folder, filename), index=False)


def create_raw_aggregate_fix_rate(test_data, filename):
    test_result_codes = test_data.iloc[:, 9].value_counts()
    aggregate_raw_fix_rate = pd.DataFrame(test_result_codes).transpose()
    aggregate_raw_fix_rate.to_excel(os.path.join(result_sheet_folder, filename), index=False)


def create_fix_probability(test_data, filename):
    group_columns = test_data.columns[:9].tolist()
    result_column = test_data.columns[9]
    # Group by the specified columns
    grouped = test_data.groupby(group_columns)
    # Calculate the new columns
    fix_rate_data = grouped[result_column].agg(
        fix_probability=lambda x: (x == 0).mean(),
        fix_patch_count=lambda x: (x == 0).sum(),
        total_response_count=lambda x: x.count()
    ).reset_index()

    fix_rate_data = fix_rate_data.sort_values(by='fix_probability', ascending=False)

    fix_rate_data.to_excel(os.path.join(result_sheet_folder, filename), index=False)

    return fix_rate_data


def create_fix_rate_for_each_bug(fix_rate_data, filename):
    fix_rate_for_each_bug = fix_rate_data.groupby(['Project', 'Bug_id'])[
        ['fix_patch_count', 'total_response_count']].sum().reset_index()

    fix_rate_for_each_bug.to_excel(os.path.join(result_sheet_folder, filename), index=False)

    return fix_rate_for_each_bug


def create_bitvector_fix_rate(fix_rate_data, filename):
    # Display the resulting dataframe
    fix_rate_for_bitvector = fix_rate_data.groupby(fix_rate_data.columns[2:9].tolist()).agg(
        total_fix_patch=('fix_patch_count', 'sum'),
        total_response=('total_response_count', 'sum')
    ).reset_index()
    fix_rate_for_bitvector['bitvector'] = fix_rate_for_bitvector[fix_rate_data.columns[2:9].tolist()].astype(
        str).agg(''.join, axis=1)
    grouped_df = fix_rate_for_bitvector[['bitvector', 'total_response', 'total_fix_patch']]
    grouped_df.to_excel(os.path.join(result_sheet_folder, filename), index=False)


def keep_top_k_highest_fix_rate_bitvector(input_dict, _k: int):
    # Sort the input_dict based on the length of the value dict in descending order
    sorted_dict = sorted(input_dict.items(), key=lambda x: len(x[1]), reverse=True)

    # Keep only the top 10
    top_10 = dict(sorted_dict[:_k])

    return top_10


dataset = ["106-dataset", "395-dataset", "315-dataset"]

all_success = 0

for dataset_name in dataset:
    result_sheet_folder = os.path.join("..", "training-data", "result-sheet", dataset_name)
    result_path = os.path.join(result_sheet_folder, "raw_result_strata.xlsx")

    raw_data = pd.read_excel(result_path, engine='openpyxl')

    create_raw_bitvector_fix_rate(raw_data, "raw_strata_fix_rate.xlsx")
    create_raw_aggregate_fix_rate(raw_data, "raw_aggregate_fix_rate.xlsx")
    fix_rate = create_fix_probability(raw_data, "strata_fix_probability_for_each_bug.xlsx")
    create_fix_rate_for_each_bug(fix_rate, "fix_count_for_each_bug.xlsx")
    create_bitvector_fix_rate(fix_rate, "strata_fix_count.xlsx")

    fixed_bug: dict = {}
    for index, row in fix_rate[fix_rate['fix_probability'] > 0].iterrows():
        project_bug_id = f"{row['Project']}:{row['Bug_id']}"

        # Append the project_bug_id to the set in the dictionary for the code_key
        if project_bug_id not in fixed_bug:
            fixed_bug[project_bug_id] = None

    print(f"{len(fixed_bug)} bug fixed at least in one of three response generation using a specific bitvector in {dataset_name}")

    fixed_bug: dict = list(fixed_bug.keys())

    if dataset_name == "106-dataset":
        with open(os.path.join("..", "training-data", "datasets-list", "30-106-dataset.json"), "r") as sample_bug_file:
            sample_bugs = json.load(sample_bug_file)

            for project in sample_bugs.keys():
                bugs = sample_bugs[project]
                for bid in bugs:
                    if f"{project}:{bid}" not in fixed_bug:
                        print(f"{dataset_name}: {project}-{bid} is not fixed by any bitvector")
    elif dataset_name == "395-dataset":
        with open(os.path.join("..", "training-data", "datasets-list", "30-395-dataset.json"), "r") as sample_bug_file:
            sample_bugs = json.load(sample_bug_file)

            for project in sample_bugs.keys():
                bugs = sample_bugs[project]
                for bid in bugs:
                    if f"{project}:{bid}" not in fixed_bug:
                        print(f"{dataset_name}: {project}-{bid} is not fixed by any bitvector")

    fixed_bug: dict = {}
    for index, row in fix_rate[fix_rate['fix_probability'] > 0].iterrows():
        project_bug_id = f"{row['Project']}:{row['Bug_id']}"
        code_key = ''.join(row.iloc[2:9].astype(str))

        # Append the project_bug_id to the set in the dictionary for the code_key
        if project_bug_id not in fixed_bug:
            fixed_bug[project_bug_id] = {}

        fixed_bug[project_bug_id][code_key] = row['fix_probability']

    for bug in fixed_bug.keys():
        bitvectors: dict = fixed_bug[bug]
        if "1111111" in bitvectors or "1000000" in bitvectors.keys():
            continue

        all_success_bitvectors = bitvectors.copy()

        # keys_to_remove = []
        # for key, value in all_success_bitvectors.items():
        #     if value != 1:
        #         keys_to_remove.append(key)
        #
        # for key in keys_to_remove:
        #     del all_success_bitvectors[key]
        #
        # if len(all_success_bitvectors) == 0:
        #     continue
        #
        # print(f"{dataset_name} {bug} can be fixed by {len(all_success_bitvectors)} bitvectors in all 3 generation"
        #       f", but not with all facts or only buggy function. They are:")
        # print(all_success_bitvectors.keys())
        # print()

    if all_success == 0:
        fix_succeed = fix_rate[fix_rate['fix_probability'] > 0]
    else:
        fix_succeed = fix_rate[fix_rate['fix_probability'] == 1]

    result_dict: dict = {}

    # Iterate through each row of the filtered DataFrame
    for index, row in fix_succeed.iterrows():
        # Concatenate the values of columns 3 to 19 as the code key
        code_key = ''.join(row.iloc[2:9].astype(str))

        # Create the project_bug_id string
        project_bug_id = f"{row['Project']}:{row['Bug_id']}"

        # Append the project_bug_id to the set in the dictionary for the code_key
        if code_key not in result_dict:
            result_dict[code_key] = {project_bug_id}
        else:
            # If the code_key is already in the dictionary, add the new project_bug_id
            result_dict[code_key].add(project_bug_id)

    if all_success == 0:
        k = 3
    else:
        k = 5

    top_10_bitvector: dict = keep_top_k_highest_fix_rate_bitvector(result_dict, k)

    if "1111111" not in top_10_bitvector:
        top_10_bitvector["1111111"] = result_dict["1111111"]
    if "1000000" not in top_10_bitvector:
        top_10_bitvector["1000000"] = result_dict["1000000"]

    upset_data: DataFrame = upsetplot.from_contents(top_10_bitvector)

    # Create an UpSet plot
    ax = upsetplot.plot(upset_data, subset_size='count', show_counts='%d', sort_by="cardinality")

    if all_success == 0:
        plt.savefig(os.path.join(result_sheet_folder, "best_of_3_strata_fix_rate_upset.png"))
    else:
        plt.savefig(os.path.join(result_sheet_folder, "all_success_strata_fix_rate_upset.png"))

    plt.show()


# all_keys = list(result_dict.keys())
# intersections = {}
#
# for i in range(1, len(result_dict) + 1):
#     for subset in combinations(all_keys, i):
#         common_elements = set.intersection(*[result_dict[key] for key in subset])
#         if common_elements:
#             intersections[subset] = common_elements
#
# # Print intersections and their elements
# for subset, elements in intersections.items():
#     print(f"Intersection {subset}: {len(elements)} elements - {', '.join(elements)}")
