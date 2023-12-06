import os.path
import pandas as pd


stratum = "second"
result_path = os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_result.xlsx")

test_data = pd.read_excel(result_path, engine='openpyxl')

test_results = test_data["Pass Test"]

test_data['bitvector'] = test_data.iloc[:, 2:19].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

# Group by the 'bitvector' and count the values in column 19
grouped_by_bitvector = test_data.groupby(['bitvector', test_data.columns[19]]).size().unstack(fill_value=0)

# Reset index to make 'bitvector' a column
bitvector_raw_fix_rate = grouped_by_bitvector.reset_index()

bitvector_raw_fix_rate.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_bitvecotr_fix_rate.xlsx"), index=False)

test_result_codes = test_data.iloc[:, 19].value_counts()
aggregate_raw_fix_rate = pd.DataFrame(test_result_codes).transpose()
aggregate_raw_fix_rate.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_raw_aggregate_fix_rate.xlsx"), index=False)


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

fix_rate_for_each_bug = fix_rate_data.groupby(['Project', 'Bug_id'])[['fix_patch_count', 'total_response_count']].sum().reset_index()
fix_rate_for_each_bug.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_fix_rate_for_each_bug.xlsx"), index=False)


fix_rate_for_each_bug = fix_rate_data.groupby(['Project', 'Bug_id']).agg(
    total_fix_patch=('fix_patch_count', 'sum'),
    total_count=('total_response_count', 'sum')
).reset_index()

# Display the resulting dataframe


fix_rate_for_bitvector = fix_rate_data.groupby(fix_rate_data.columns[2:19].tolist()).agg(
    total_fix_patch=('fix_patch_count', 'sum'),
    total_count=('total_response_count', 'sum')
).reset_index()


fix_rate_for_bitvector['unique_code'] = fix_rate_for_bitvector[fix_rate_data.columns[2:19].tolist()].astype(str).agg(''.join, axis=1)
grouped_df = fix_rate_for_bitvector[['unique_code', 'total_count', 'total_fix_patch']]

grouped_df.to_excel(os.path.join("..", "preliminary-study", f"{stratum}_stratum_bitvector_fix_rate.xlsx"), index=False)

