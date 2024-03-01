### Bug Analysis:
- The bug occurs when the function `_unstack_multiple` is trying to unstack a DataFrame with a MultiIndex where one of the levels has tuple names.
- The `clocs` parameter passed to the function contains tuple names like `(('A', 'a'), 'B')`.
- The bug arises because the function erroneously assumes that it can directly use the level names from the index to identify the levels to unstack. This assumption fails when dealing with tuple names.
- The error message indicates that the function is not properly handling the tuple names when trying to get their level numbers.

### Bug Fix Strategy:
- Update the function to correctly handle tuple names by checking for tuple types and extracting level names from tuples to get their level numbers.
- Modify the logic for getting level numbers to accommodate tuples within `clocs`.
- Ensure that the function correctly handles the scenario where tuple names are involved in identifying levels for unstacking.

### Corrected Function:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs_levelnums = []
    for loc in clocs:
        if isinstance(data.index, MultiIndex):
            level_name = loc[0] if isinstance(loc, tuple) else loc
            clocs_levelnums.append(data.index._get_level_number(level_name))
        else:
            clocs_levelnums.append(loc)

    rlocs = [i for i in range(index.nlevels) if i not in clocs_levelnums]

    clevels = [index.levels[i] for i in clocs_levelnums]
    ccodes = [index.codes[i] for i in clocs_levelnums]
    cnames = [index.names[i] for i in clocs_levelnums]
    rlevels = [index.levels[i] for i in rlocs]
    rcodes = [index.codes[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    # Rest of the function remains the same...

```

### Summary:
- The corrected function above includes the necessary changes to handle tuple names when determining level numbers within the MultiIndex.
- This modification should address the issue reported on GitHub and allow the function to correctly unstack DataFrames with MultiIndex containing tuple names.