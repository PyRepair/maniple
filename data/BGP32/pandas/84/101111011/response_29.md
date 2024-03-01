### Bug Explanation
The bug occurs because the `clocs` variable is being incorrectly created by passing a tuple `(('A', 'a'), 'B')` instead of expected integers to represent the levels. Hence, the function fails to retrieve the correct level number using `index._get_level_number(i)` leading to errors in generating the `clocs` list for further processing.

### Fixing the Bug
To fix the bug, we need to modify how the `clocs` variable is created to contain the correct level indices based on the input tuple names. The function `_unstack_multiple` needs to handle the case where the input is a tuple of names and transform it into the appropriate index values before processing.

### Corrected Function
Here is the corrected version of the `_unstack_multiple` function:

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index.get_level_number(i) if isinstance(i, tuple) else i for i in clocs]  # Modify clocs for tuple names

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

    # The remaining contents of the function remains the same
    ...
```

This correction allows the function to handle cases where the input tuple names need to be converted into level indices before further processing.

By implementing this change, the function is now able to correctly process the input tuple names and avoid the KeyError that was occurring before.