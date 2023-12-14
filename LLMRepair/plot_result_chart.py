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
    fix_rate_data.to_excel(os.path.join(result_sheet_folder, filename), index=False)

    return fix_rate_data


def create_fix_rate_for_each_bug(fix_rate_data, filename):
    fix_rate_for_each_bug = fix_rate_data.groupby(['Project', 'Bug_id'])[
        ['fix_patch_count', 'total_response_count']].sum().reset_index()
    fix_rate_for_each_bug.to_excel(os.path.join(result_sheet_folder, filename), index=False)


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


def keep_top_5_highest_fix_rate_bitvector(input_dict):
    # Sort the input_dict based on the length of the value dict in descending order
    sorted_dict = sorted(input_dict.items(), key=lambda x: len(x[1]), reverse=True)

    # Keep only the top 10
    top_10 = dict(sorted_dict[:5])

    return top_10


dataset_name = "395-dataset"
database_path = os.path.join("..", "training-data", dataset_name)
result_sheet_folder = os.path.join("..", "training-data", "result-sheet", dataset_name)
result_path = os.path.join(result_sheet_folder, "raw_result_strata.xlsx")

raw_data = pd.read_excel(result_path, engine='openpyxl')

create_raw_bitvector_fix_rate(raw_data, "raw_strata_fix_rate.xlsx")
create_raw_aggregate_fix_rate(raw_data, "raw_aggregate_fix_rate.xlsx")
fix_rate = create_fix_probability(raw_data, "strata_fix_probability_for_each_bug.xlsx")
create_fix_rate_for_each_bug(fix_rate, "fix_rate_for_each_bug.xlsx")
create_bitvector_fix_rate(fix_rate, "strata_fix_rate.xlsx")


fix_succeed = fix_rate[fix_rate['fix_probability'] > 0]

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

top_10_bitvector = keep_top_5_highest_fix_rate_bitvector(result_dict)

if "1111111" not in top_10_bitvector:
    top_10_bitvector["1111111"] = result_dict["1111111"]
if "1000000" not in top_10_bitvector:
    top_10_bitvector["1000000"] = result_dict["1000000"]


upset_data: DataFrame = upsetplot.from_contents(top_10_bitvector)

# Create an UpSet plot
ax = upsetplot.plot(upset_data, subset_size='count', show_counts='%d', sort_by="cardinality")

plt.savefig(os.path.join(result_sheet_folder, "strata_fix_rate_upset.png"))
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
