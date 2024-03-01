### Bug Explanation:
The bug occurs due to the use of a tuple as the level parameter in the `unstack` function. When a MultiIndex is created with tuple names and then unstacked using a tuple as the level parameter, the `_get_level_number` method fails to retrieve the correct level number since it expects the level parameter to be a string (level name) rather than a tuple.

### Solution Strategy:
To fix the bug, we need to ensure that the level parameter passed to `_get_level_number` is a string representing the level name, not a tuple. We can modify the function to extract the correct level name from the tuple if it is passed as a parameter.

### Corrected Function:

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    # Convert any tuple level names to a string level name
    clocs = [i if not isinstance(i, tuple) else i[0] for i in clocs]

    # Rest of the function remains the same
    rlocs = [i for i in range(index.nlevels) if i not in clocs]
    
    clocs = [index._get_level_number(i) for i in clocs]

    clevels = [index.levels[i] for i in clocs]
    ccodes = [index.codes[i] for i in clocs]
    cnames = [index.names[i] for i in clocs]
    rlevels = [index.levels[i] for i in rlocs]
    rcodes = [index.codes[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    # Rest of the function implementation
    ...
```

The correction involves converting tuple level names to string level names before passing them to `_get_level_number`. This modification ensures that the correct level number is retrieved and resolves the `Level A not found` KeyError issue.

After applying these changes, the unstack operation should work correctly with tuple names in the MultiIndex.