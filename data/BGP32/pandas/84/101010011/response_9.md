### Bug Analysis:
- The function `_get_level_number` is expected to return the level number for a given level name in a MultiIndex object.
- The error messages show that the KeyError or ValueError is raised because the level name being provided is not being found in the list of names of the MultiIndex.
- The bug arises because the method `_get_level_number` is mistakenly looking for the tuple of names instead of a single name in the list while trying to extract the level number.
- As a result, fixing this issue requires ensuring that we correctly process and handle the level names.

### Bug Fix Strategy:
- Modify the `_get_level_number` method to correctly handle single-level and multi-level names.
- Ensure the correct extraction of the level number regardless of the type (single name or tuple of names).

### Corrected Function:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index._get_level_number(i) if isinstance(i, tuple) else index.names.index(i) for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    clevels = [index.levels[i] for i in clocs]
    ccodes = [index.codes[i] for i in clocs]
    cnames = [index.names[i] for i in clocs]
    rlevels = [index.levels[i] for i in rlocs]
    rcodes = [index.codes[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    # Rest of the function code remains the same
```

By incorporating this correction in the `_unstack_multiple` function, the code should now correctly handle the extraction of level numbers for both single-level names and tuple names in MultiIndex objects. This fix should resolve the KeyError and ValueError issues encountered in the failing tests.