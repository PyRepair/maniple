You have been provided with a description for GitHub issue. However, it may be ambiguous, please simplify it and make it readable by developer while keeping the key information.

Here is an example summary of a GitHub issue:

GitHub Bug Title:
TypeError when calling mean on a DataFrameGroupBy with Int64 dtype

Description:
Using the new nullable integer data type, calling mean after grouping results in a TypeError. It works with int64 dtype and also with Int64 dtype when taking a single column to give a SeriesGroupBy. The error occurs with median and std as well. However, it does not occur with min, max, or first.

Expected Output:
When performing aggregation operations on a DataFrameGroupBy object with columns of nullable integer data type (Int64), the following behaviours are expected for the specified methods:
mean(): The method should compute the mean of grouped data without raising a TypeError.
median():The method should compute the median of grouped data without raising a TypeError.
std(): The method should compute the standard deviation of grouped data without raising a TypeError.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0