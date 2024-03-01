### Bug Analysis:
The bug occurs when the `_unstack_multiple` function is trying to get the level number for a multi-level index but encounters an error when the level name is not found in the list of names.

### Bug Explanation:
- The error arises from the line `clocs = [index._get_level_number(i) for i in clocs]` where `clocs` contains the tuple `(('A', 'a'), 'B')`.
- The `_get_level_number` function tries to find the index of the level name in `index.names` but throws an error when it doesn't find it.
- The error message indicates that `'A' is not in list`, indicating that 'A' is not present as a level name.

### Bug Fix:
To fix the bug, we need to ensure that the function correctly handles multi-level names and doesn't error out when searching for a level name.

### Corrected Function:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    cloc_numbers = []
    for cloc in clocs:
        if isinstance(cloc, tuple):
            level_names = [lvl.name for lvl in index.levels]
            cloc_num = [idx for idx, names in enumerate(level_names) if set(cloc) == set(names)]
            if not cloc_num:
                raise KeyError(f"Level {cloc} not found")
            cloc_numbers.extend(cloc_num)
        else:
            cloc_numbers.append(index._get_level_number(cloc))

    rlocs = [i for i in range(index.nlevels) if i not in cloc_numbers]
    
    # Remaining function code…
```

Now, the function includes a check to handle cases where the `cloc` is a tuple of level names. If the matching levels are found, their corresponding numbers are added to `cloc_numbers`. Otherwise, a `KeyError` is raised.

This change ensures that the function can handle multi-level names correctly without encountering errors when looking for level numbers.