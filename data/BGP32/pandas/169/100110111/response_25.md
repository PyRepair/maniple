### Analysis:
1. The `quantile` function is supposed to compute quantiles for a DataFrame along a specified axis. The function has multiple parameters like quantile `q`, axis, `numeric_only`, and interpolation method.
   
2. The failed test `test_quantile_empty_no_columns` provides an empty DataFrame without columns, and attempts to compute quantiles on it.
   
3. The error message suggests a concatenation issue in `_concat_compat` function in the code, pointing towards a problem when trying to concatenate the blocks in `_concat_compat`.

### Error Location:
The error seems to occur when trying to concatenate empty blocks of data.

### Bug Cause:
The implementation fails to handle the case of an empty DataFrame, specifically when no data is available for quantile computation.

### Fix Strategy:
To resolve this issue, a check for empty dataframes can be added, and an early return or alternative computation method can be implemented to handle this scenario.

### Updated Function:
```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    if self.empty:
        if isinstance(q, float):
            result = pd.Series([])
            result.name = q
            result.index.name = self.columns.name
        else:
            result = pd.DataFrame([], index=q, columns=[])
            result.columns.name = self.columns.name
        return result

    data = self._get_numeric_data() if numeric_only else self
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

With this updated function, the issue with empty DataFrames causing concatenation errors should be resolved, and the function should now handle such scenarios gracefully.