### Fixing the bug

#### Bug identified:
The bug occurs due to the `_get_numeric_data()` method returning an empty DataFrame when all columns contain non-numeric data. This causes an issue when trying to concatenate the blocks in the `quantile` function, leading to a `ValueError` - "need at least one array to concatenate".

#### Strategy for fixing the bug:
To fix the bug, we need to handle the case where all columns in the DataFrame are non-numeric correctly. We can modify the logic to return an appropriate empty DataFrame or empty Series instead of causing a concatenation error.

#### Revised `quantile` function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)

    data = self._get_numeric_data()
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if data.empty:
        if q != 0.5:
            return self._constructor(result)
        else:
            if isinstance(q, (int, float)) or len(q) == 1:
                return pd.Series([], name=q)
            else:
                return pd.DataFrame([], index=q)

    if is_transposed:
        data = data.T

    result = data._data.quantile(q=q, axis=1, interpolation=interpolation, transposed=is_transposed)

    if result.ndim == 2:
        result = self._constructor(result)
    else:
        result = self._constructor_sliced(result, name=q)

    if is_transposed:
        result = result.T

    return result
```

By updating the `quantile` function as shown above, we handle the scenario of all columns being non-numeric data correctly, preventing the concatenation error and ensuring the function works as expected even with empty or non-numeric data columns.