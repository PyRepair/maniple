### Issue Analysis
The issue arises when attempting to unstack a MultiIndexed DataFrame with tuple names. The `unstack` operation fails with a `KeyError` because the function `_get_level_number` within the `pandas` library doesn't handle tuple names correctly, leading to the error message `'Level A not found'`.

### Bug Location
The bug originates in the `_unstack_multiple` function's handling of the `clocs` parameter by trying to access the level number based on a tuple name. The index extraction for levels is improperly handling tuple names leading to the `KeyError`.

### Bug Explanation
The function `_unstack_multiple` incorrectly assumes that `clocs` is an index to extract the level number without considering that the index could include tuples for MultiIndex columns. This error results in trying to access a tuple value as an index level, leading to the reported KeyError issue.

### Bug Fix Strategy
To fix the bug, we need to update the code in `_unstack_multiple` to handle tuple names properly when extracting the level number. This can be achieved by checking the type of `i` and modifying the index extraction logic accordingly.

### Corrected Code
Here is the corrected version of the `_unstack_multiple` function:

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    clevels = [index.levels[i] if isinstance(index, MultiIndex) else index._get_level_values(i) for i in clocs]
    rlevels = [index.levels[i] if isinstance(index, MultiIndex) else index._get_level_values(i) for i in rlocs]

    if rlocs == []:
        # Everything is in clocs, so the dummy df has a regular index
        dummy_index = Index(obs_ids, name="__placeholder__")
    else:
        dummy_index = MultiIndex(
            levels=rlevels + [obs_ids],
            codes=rcodes + [comp_ids],
            names=([index.names[i] if isinstance(index, MultiIndex) else index.names[i][0] for i in rlocs] + ["__placeholder__"]),
            verify_integrity=False
        )

    if isinstance(data, Series):
        dummy = data.copy()
        dummy.index = dummy_index

        unstacked = dummy.unstack("__placeholder__", fill_value=fill_value)
        new_levels = clevels
        new_names = [index.names[i] if isinstance(index, MultiIndex) else index.names[i][0] for i in clocs]
        new_codes = recons_codes
    else:
        if isinstance(data.columns, MultiIndex):
            result = data
            for i in range(len(clocs)):
                val = clocs[i]
                result = result.unstack(val, fill_value=fill_value)
                clocs = [v if i > v else v - 1 for v in clocs]

            return result

        dummy = data.copy()
        dummy.index = dummy_index

        unstacked = dummy.unstack("__placeholder__", fill_value=fill_value)
        if isinstance(unstacked, Series):
            unstcols = unstacked.index
        else:
            unstcols = unstacked.columns
        new_levels = [unstcols.levels[0]] + clevels
        new_names = [data.columns.name] + [index.names[i] if isinstance(index, MultiIndex) else index.names[i][0] for i in clocs]

        new_codes = [unstcols.codes[0]]
        for rec in recons_codes:
            new_codes.append(rec.take(unstcols.codes[-1]))

    new_columns = MultiIndex(
        levels=new_levels, codes=new_codes, names=new_names, verify_integrity=False
    )

    if isinstance(unstacked, Series):
        unstacked.index = new_columns
    else:
        unstacked.columns = new_columns

    return unstacked
```

This corrected version should handle the tuple names correctly and resolve the KeyError issue during the unstack operation on MultiIndexed DataFrames with tuple names.