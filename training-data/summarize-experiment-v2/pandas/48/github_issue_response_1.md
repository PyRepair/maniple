GitHub Bug Title:
Calling mean on a DataFrameGroupBy with Int64 dtype results in TypeError

Description:
When using the new nullable integer data type and calling mean after grouping, a TypeError occurs. It works with int64 dtype as well as with Int64 dtype when taking a single column to give a SeriesGroupBy. The error occurs with median and std as well, but does not occur with min, max, or first.

Expected Output:
When performing aggregation operations on a DataFrameGroupBy object with columns of nullable integer data type (Int64), the following behaviours are expected for the specified methods:
mean(): The method should compute the mean of grouped data without raising a TypeError.
median(): The method should compute the median of grouped data without raising a TypeError.
std(): The method should compute the standard deviation of grouped data without raising a TypeError.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0