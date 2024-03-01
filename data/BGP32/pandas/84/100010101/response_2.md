### Bug analysis:
1. The function is intended to unstack a DataFrame based on specified column locations (`clocs`).
2. The bug occurs in the conversion of column locations (`clocs`) to numerical values using `_get_level_number` method of the index.
3. The error message states that an incorrect lookup of the level `'A'` occurs in the list of names.
4. The bug arises from incorrect handling of MultiIndex levels in the `_get_level_number` method.

### Bug fix strategy:
1. Instead of passing a tuple of strings as column locations, convert the tuple to a list of integers representing MultiIndex level numbers.
2. Update the code to correctly map column locations to the respective level numbers.
3. Handle the exception gracefully, especially in cases where the column locations are part of a MultiIndex.

### Corrected function:

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    # Convert column locations to numeric level numbers
    clocs = [index._get_level_number(loc) if isinstance(loc, tuple) else loc for loc in clocs]

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
    # ...
```

By fixing the conversion of column locations to numeric level numbers and ensuring proper handling for MultiIndex cases, the corrected function should now work as expected without causing the previous errors.