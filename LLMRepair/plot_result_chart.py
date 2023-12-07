import os.path
from itertools import combinations

import pandas as pd
import upsetplot
from upsetplot import UpSet, from_contents
from collections import Counter
from matplotlib import pyplot as plt


def create_raw_bitvector_fix_rate(test_data):
    test_data['bitvector'] = test_data.iloc[:, 2:19].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
    # Group by the 'bitvector' and count the values in column 19
    grouped_by_bitvector = test_data.groupby(['bitvector', test_data.columns[19]]).size().unstack(fill_value=0)
    # Reset index to make 'bitvector' a column
    bitvector_raw_fix_rate = grouped_by_bitvector.reset_index()
    bitvector_raw_fix_rate.to_excel(
        os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_bitvecotr_fix_rate.xlsx"), index=False)


def create_raw_aggregate_fix_rate(test_data):
    test_result_codes = test_data.iloc[:, 19].value_counts()
    aggregate_raw_fix_rate = pd.DataFrame(test_result_codes).transpose()
    aggregate_raw_fix_rate.to_excel(
        os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_aggregate_fix_rate.xlsx"), index=False)


def create_fix_probability(test_data):
    group_columns = test_data.columns[:19].tolist()
    result_column = test_data.columns[19]
    # Group by the specified columns
    grouped = test_data.groupby(group_columns)
    # Calculate the new columns
    fix_rate_data = grouped[result_column].agg(
        fix_probability=lambda x: (x == 0).mean(),
        fix_patch_count=lambda x: (x == 0).sum(),
        total_response_count=lambda x: x.count()
    ).reset_index()
    fix_rate_data.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_fix_rate.xlsx"), index=False)

    return fix_rate_data


def create_fix_rate_for_each_bug(fix_rate_data):
    fix_rate_for_each_bug = fix_rate_data.groupby(['Project', 'Bug_id'])[
        ['fix_patch_count', 'total_response_count']].sum().reset_index()
    fix_rate_for_each_bug.to_excel(
        os.path.join("..", "preliminary-study", f"{stratum}_stratum_fix_rate_for_each_bug.xlsx"), index=False)


def create_bitvector_fix_rate(fix_rate_data):
    # Display the resulting dataframe
    fix_rate_for_bitvector = fix_rate_data.groupby(fix_rate_data.columns[2:19].tolist()).agg(
        total_fix_patch=('fix_patch_count', 'sum'),
        total_response=('total_response_count', 'sum')
    ).reset_index()
    fix_rate_for_bitvector['bitvector'] = fix_rate_for_bitvector[fix_rate_data.columns[2:19].tolist()].astype(
        str).agg(''.join, axis=1)
    grouped_df = fix_rate_for_bitvector[['bitvector', 'total_response', 'total_fix_patch']]
    grouped_df.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_bitvector_fix_rate.xlsx"),
                        index=False)


stratum = "first"
result_path = os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_result.xlsx")

raw_data = pd.read_excel(result_path, engine='openpyxl')


create_raw_bitvector_fix_rate(raw_data)
create_raw_aggregate_fix_rate(raw_data)
fix_rate = create_fix_probability(raw_data)
create_fix_rate_for_each_bug(fix_rate)
create_bitvector_fix_rate(fix_rate)

fix_succeed = fix_rate[fix_rate['fix_probability'] > 0]

# If you need to work with the filtered data or export it:
# You can work with `df_filtered` as needed or export it to a new CSV

result_dict: dict = {}

# Iterate through each row of the filtered DataFrame
for index, row in fix_succeed.iterrows():
    # Concatenate the values of columns 3 to 19 as the code key
    code_key = ''.join(row.iloc[2:19].astype(str))

    # Create the project_bug_id string
    project_bug_id = f"{row['Project']}:{row['Bug_id']}"

    # Append the project_bug_id to the set in the dictionary for the code_key
    if code_key not in result_dict:
        result_dict[code_key] = {project_bug_id}
    else:
        # If the code_key is already in the dictionary, add the new project_bug_id
        result_dict[code_key].add(project_bug_id)



# Inverting the data structure: Each unique value (e.g., "youtube-dl:17") becomes a key,
# and the set of unique codes where it appears will be the value
inverted_data = {}

# # Populate the inverted data structure
# for set_code, items in result_dict.items():
#     for item in items:
#         if item not in inverted_data:
#             inverted_data[item] = set()
#         inverted_data[item].add(set_code)
#
# # Display the inverted data
# upset_data = from_contents(inverted_data)
#
# # Creating the UpSet plot
# upset = UpSet(upset_data, subset_size='count', show_counts=True)
# upset.plot()
# plt.suptitle("UpSet Plot of Inverted Data")
# plt.show()


upset_data = upsetplot.from_contents(result_dict)

# Create an UpSet plot
ax = upsetplot.plot(upset_data, subset_size='count', show_counts='%d', sort_by="cardinality")

# Calculate intersections
all_keys = list(result_dict.keys())
intersections = {}

for i in range(1, len(result_dict) + 1):
    for subset in combinations(all_keys, i):
        common_elements = set.intersection(*[result_dict[key] for key in subset])
        if common_elements:
            intersections[subset] = common_elements

# Print intersections and their elements
for subset, elements in intersections.items():
    print(f"Intersection {subset}: {len(elements)} elements - {', '.join(elements)}")

plt.show()
