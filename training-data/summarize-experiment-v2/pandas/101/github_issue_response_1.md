GitHub Bug Title:
Categorical to int conversion ignores NaNs

Description:
When converting a categorical series to an integer column, NaN values are converted to incorrect integer negative values. This behavior is unexpected and results in errors when trying to use d.astype('Int8').

Expected Output:
When converting categorical series to IntX (nullable integer) or float, NaN values should be preserved and represented as NaN.

Environment:
- Python: 3.7.4.final.0
- pandas: 0.25.1
- numpy: 1.17.2