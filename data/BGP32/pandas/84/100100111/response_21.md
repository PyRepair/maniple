### Bug Analysis:
1. The `_get_level_number` method is used to retrieve the index level number based on the level name, but it fails due to the incorrect handling of multi-level names.
2. The bug arises because the function does not properly support hierarchical columns in multi-index, which results in a KeyError when attempting to access and unstack from an incorrect level.

### Bug Fix Strategy:
1. Modify the `_get_level_number` section to correctly handle multi-level names in the index.
2. Ensure that the function can handle both single-level and multi-level index names for unstacking operation.
3. Update the code to support the unstacking operation for multi-index with tuple names.

### Corrected Function Code:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    def get_level_number(level):
        if not isinstance(level, int):
            return index.names.index(level)
        return level

    clocs = [get_level_number(i) for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    ...

```

Applying the corrections as shown above, the function will be able to properly handle multi-level index names and perform the unstacking operation as expected.