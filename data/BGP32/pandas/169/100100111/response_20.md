### Bug Explanation:
The bug occurs because the `_get_numeric_data()` method, used to filter out non-numeric columns from the DataFrame, ends up returning an empty DataFrame when all columns are non-numeric (in this case, all columns are datetime columns). This results in issues down the line in the `quantile()` function since it expects numerical data to perform calculations.

### Bug Location:
The bug is primarily located in the logic where the DataFrame's numeric data is extracted using `_get_numeric_data()` and later processed without properly handling scenarios where no numeric data is present.

### Bug Fix Strategy:
To fix the bug, we need to adjust the logic to handle cases where all columns are non-numeric (e.g., datetime columns). One approach could be to update the function to fall back to the original DataFrame when no numeric data is found, allowing quantile calculation on non-numeric data as well.

### Corrected Function:
Below is the corrected version of the `quantile()` function that addresses the issue:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()

    if data.empty:  # Check if all columns are non-numeric
        data = self
        numeric_only = False

    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if is_transposed:
        data = data.T

    result = data._data.quantile(
        qs=q, axis=1, interpolation=interpolation, transposed=is_transposed
    )

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

The corrected version of the function now checks if the extracted numeric data is empty and, if so, uses the original DataFrame `self` instead. This ensures that the quantile calculation can handle both numeric and non-numeric data.

By making this adjustment, the function should now pass the failing test case and provide the expected output described in the GitHub issue.