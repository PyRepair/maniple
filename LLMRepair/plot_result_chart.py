import os.path
import pandas as pd


result_path = os.path.join("..", "preliminary-study", "first_stratum_raw_result.xlsx")

test_data = pd.read_excel(result_path, engine='openpyxl')

test_results = test_data["Pass Test"]

test_data['bitvector'] = test_data.iloc[:, 2:18].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

# Group by the 'bitvector' and count the values in column 19
grouped_by_bitvector = test_data.groupby(['bitvector', test_data.columns[19]]).size().unstack(fill_value=0)

# Reset index to make 'bitvector' a column
bitvector_fix_rate = grouped_by_bitvector.reset_index()

bitvector_fix_rate.to_excel(os.path.join("..", "preliminary-study", "bitvecotr_fix_rate.xlsx"), index=False)


test_result_codes = test_data.iloc[:, 19].value_counts()
aggregate_fix_rate = pd.DataFrame(test_result_codes).transpose()
aggregate_fix_rate.to_excel(os.path.join("..", "preliminary-study", "aggregate_fix_rate.xlsx"), index=False)


