GitHub Bug Title:
TypeError when calling mean on a DataFrameGroupBy with Int64 dtype

Description:
Using the new nullable integer data type, calling mean after grouping results in a TypeError. It works with int64 dtype and also with Int64 dtype when taking a single column to give a SeriesGroupBy. The error occurs with median and std as well. However, it does not occur with min, max, or first.

Expected Output:
The expected output should be the mean of column 'b' grouped by column 'a' as shown in the provided description.

Environment:
- Python: 3.7.3.final.0
- pandas: 1.0.1
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0