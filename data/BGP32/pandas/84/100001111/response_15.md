### Bug Explanation
The bug in the `_unstack_multiple` function is caused by the way it handles the input `clocs` which is a tuple of column names. The function expects `clocs` to be a list of integers corresponding to the column levels, but in the failing tests, it receives a tuple of column names which leads to a KeyError when trying to convert those names to level numbers.

### Bug Fixing Strategy
To fix the bug, the function should handle the case where `clocs` is a tuple of column names by converting the column names to level numbers correctly before proceeding with unstacking.

### Corrected Function
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index._get_level_number(i) if isinstance(i, tuple) else i for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    # The rest of the function remains the same
```

With this change, the function correctly handles cases where `clocs` is a tuple of column names and converts them to level numbers before continuing with the unstacking process.