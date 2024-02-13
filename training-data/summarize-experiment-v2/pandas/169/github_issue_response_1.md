GitHub Bug Title:
TypeError when calling mean on a DataFrameGroupBy with Int64 dtype

Description:
When using the new nullable integer data type, calling mean after grouping results in a TypeError. The error also occurs with median and std but does not occur with min, max, or first.

Expected Output:
When performing aggregation operations on a DataFrameGroupBy object with columns of nullable integer data type (Int64), the mean, median, and std methods should compute the values without raising a TypeError.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0