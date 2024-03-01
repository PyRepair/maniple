### Bug Explanation
The bug arises from the `_get_level_number` function where it expects a string input representing a level but receives a tuple instead. This causes a `KeyError` when trying to find the level, as it searches for a string in the list of level names.

### Bug Fix Strategy
1. Modify the `clocs` variable so that it contains only strings representing level names instead of tuples.
2. Use the modified `clocs` list to access the level numbers correctly.

### Corrected Version
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    clocs = [index._get_level_number(i) if isinstance(i, str) else i for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    # Rest of the code remains the same
```

This modification ensures that only strings are used to find index level numbers, avoiding the `KeyError` issue. It fixes the bug related to unstacking in the presence of tuple names for levels.