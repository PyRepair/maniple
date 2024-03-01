### Bug Analysis:
The bug occurs in the function `quantile` when handling empty DataFrames, causing a ValueError due to attempting to concatenate empty arrays. The error message specifically indicates that there are no arrays to concatenate.

### Bug Location:
The bug is likely located in the section where the `quantile` function tries to process the empty DataFrame. The issue might arise from how the function attempts to manipulate and process data in this specific scenario.

### Bug Cause:
1. When an empty DataFrame is passed to the `quantile` function, it fails to handle the case of empty data properly.
2. The function continues to process the empty DataFrame and attempts to concatenate arrays, which results in a ValueError.

### Bug Fix Strategy:
To fix the bug, we need to enhance the handling of empty DataFrames within the `quantile` function. If all columns are dropped by `_get_numeric_data`, then the function should return appropriate empty objects without attempting any further computations that involve concatenation.

### Corrected Function:

```python
def quantile(self, q=0.5, axis=0, numeric_only=True, interpolation="linear"):
    self._check_percentile(q)
    
    data = self._get_numeric_data() if numeric_only else self
    axis = self._get_axis_number(axis)
    is_transposed = axis == 1

    if data.empty:
        if isinstance(q, (list, np.ndarray)):
            result = pd.DataFrame([], index=q, columns=[])
        else:
            result = pd.Series([], index=[], name=q)
        
        result.index.name = self.columns.name
        return result

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

After applying this fix, the `quantile` function should now be able to correctly handle cases where the input DataFrame is empty. This corrected version should pass the failing test cases and fulfill the expected input/output values.