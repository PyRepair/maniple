Class docstring: This `dispatch_to_series` function is used to evaluate the frame operation `func(left, right)` by dispatching the operation to the Series implementation column-by-column.

`column_op(a, b)`: This function appears to be used within the `dispatch_to_series` function to perform column-wise operations. It takes two parameters `a` and `b` and returns the result of applying the `func` operation to each column.

`import pandas.core.computation.expressions as expressions`: The `dispatch_to_series` function imports the `expressions` module, suggesting that it may be used to evaluate the column-wise operations.

The function `dispatch_to_series` seems to have different logic paths based on the type of `right` parameter, as it handles scalar, DataFrame, and Series cases differently. The `column_op` function is used to perform the actual operation on the columns in different scenarios. There are also assertions to ensure that the shapes of the DataFrames and Series are compatible. The function concludes by evaluating the column operations and returning the new data.