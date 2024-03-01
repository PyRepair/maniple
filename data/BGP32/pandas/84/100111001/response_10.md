### Bug Explanation
The bug occurs because the function `_get_level_number` expects a single level name as input but is receiving a tuple of level names `(A, a)` as input. This causes the function to raise a `ValueError` indicating that the provided level name is not in the list.

### Bug Fix Strategy
To fix the bug, we need to modify how the level names are processed to ensure that `_get_level_number` receives a single level name as expected.

### Corrected Function
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    clocs = [index._get_level_number(i) if not isinstance(i, tuple) else index._get_level_number(i[0]) for i in clocs]

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

    ...
```

### Changes Made
- Modified the `clocs` list comprehension to check if the element is a tuple and fetch the first element if so before passing to `_get_level_number`.

By making this change, the function will now handle both single level names and tuples of level names correctly, fixing the bug related to level name processing.