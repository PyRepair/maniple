### Bug Explanation
The bug occurs in the `_unstack_multiple` function when trying to get the level number of a multi-index dataframe. The issue arises due to passing a tuple of names as the level parameter, which is not correctly handled in the function.

#### Problematic Line:
```python
clocs = [index._get_level_number(i) for i in clocs]
```

In the failing test cases, `clocs` is a tuple of names `(('A', 'a'), 'B')`, which is causing the function to throw a `KeyError` due to not finding the level named `'A'`.

### Bug Fix Strategy
To fix this bug, we need to modify how the `clocs` variable is processed to handle tuple names correctly. Instead of directly getting the level number using the names, we should first check if the level is an integer and then get the level number accordingly.

### Corrected Version of the Function
Here is the corrected version of the `_unstack_multiple` function:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index._get_level_number(i) if isinstance(i, str) else i for i in clocs]

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

    # Remaining code remains the same

    return unstacked
```

This correction should resolve the `KeyError` issue and allow the function to handle tuple level names correctly.