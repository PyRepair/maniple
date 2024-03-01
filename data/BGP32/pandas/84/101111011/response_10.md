### Bug Explanation
The bug is caused by the `_get_level_number` function inside the `MultiIndex` class. When attempting to unstack a MultiIndex with tuple names, the `_get_level_number` function fails to handle tuple names correctly and raises a `ValueError`. This causes subsequent issues in the `_unstack_multiple` function due to incorrect handling of the level naming.

### Bug Fix Strategy
To fix this bug, we need to modify how the level number computation is handled for MultiIndexes with tuple names. Specifically, we need to ensure that the function can handle tuple names properly when processing levels.

### Corrected Function

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    # Modify this block to correctly handle tuple names in MultiIndexes
    clocs = [
        index._get_level_number(level)
        if isinstance(level, tuple)
        else level
        for level in clocs
    ]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    clevels = [index.levels[i] for i in clocs]
    ccodes = [index.codes[i] for i in clocs]
    cnames = [index.names[i] for i in clocs]
    rlevels = [index.levels[i] for i in rlocs]
    rcodes = [index.codes[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    shape = [len(x) for x in clevels]
    group_index = get_group_index(ccodes, shape, sort=False, xnull=False)

    comp_ids, obs_ids = compress_group_index(group_index, sort=False)
    recons_codes = decons_obs_group_ids(comp_ids, obs_ids, shape, ccodes, xnull=False)

    # Rest of the function remains the same
    ...
```

By checking if the level is a tuple in the `_get_level_number` computation, we can handle tuple names correctly in MultiIndexes and prevent the function from raising errors. This modification should resolve the bugs and allow the function to work correctly for MultiIndexes with tuple names.