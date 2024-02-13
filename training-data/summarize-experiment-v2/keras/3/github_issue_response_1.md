GitHub Bug Title:
TypeError when calling mean on DataFrameGroupBy

Description:
Calling mean after grouping with nullable integer data type (Int64) results in a TypeError. The error also occurs with median and std but not with min, max, or first.

Expected Output:
Methods mean(), median(), and std() should compute the respective aggregations without raising a TypeError on DataFrameGroupBy object with nullable integer data type.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0