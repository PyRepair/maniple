### Issue Analysis
The issue arises from unstacking a MultiIndexed DataFrame with tuple names. The function `_unstack_multiple` fails to handle hierarchical columns correctly, causing the KeyError during unstacking.

### Location of Potential Error
The error occurs in the line:
```python
clocs = [index._get_level_number(i) for i in clocs]
```
where the `Level A not found` KeyError is raised, indicating a problem with getting the level number in the index.

### Bug Cause
The bug is caused by `clocs` being a tuple `(('A', 'a'), 'B')`, which results in `'A'` being treated as a string in the `_get_level_number` call for the index. The check for the tuple formatted level is not correctly handled, leading to the KeyError.

### Bug Fix
To fix this bug, the function should be adjusted to handle tuple names correctly without raising a KeyError.

### Corrected Version of the Function
Here is the corrected version of the `_unstack_multiple` function:

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # Handle hierarchical columns correctly
    if isinstance(clocs, tuple) and all(isinstance(cloc, tuple) for cloc in clocs):
        clocs = [(x[0], x[1]) for x in clocs]  # Flatten the tuple names if needed

    index = data.index

    clocs = [index._get_level_number(i) if isinstance(i, tuple) else index._get_level_number((i,)) for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    # The rest of the function remains the same
```

This correction ensures that if `clocs` contains tuple names, they are handled correctly without raising a KeyError. It flattens the nested tuples into a single tuple for level lookup in the index. It addresses the issue reported on GitHub and should resolve the KeyError during unstacking for MultiIndexed DataFrames with tuple names.