### Bug Analysis
The bug is caused by passing a tuple of mixed type names `(('A', 'a'), 'B')` as the `level` parameter to the `unstack` function, which is then passed to the `_unstack_multiple` function. The `clocs` list is being filled incorrectly with level names directly rather than their corresponding level numbers, leading to an attempt to extract the level number of name 'A', which is causing the `KeyError`.

### Bug Fix
1. Instead of passing the `level` parameter directly to `_unstack_multiple`, extract the level numbers from the names passed in `clocs`.
2. Use the extracted level numbers to perform the necessary operations.

### Corrected Code
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # Extract level numbers from level names in clocs
    index = data.index
    clocs = [index._get_level_number(i) for i in clocs]   # Extract level number

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    # Rest of the code remains unchanged
    # ...
```

Applying this fix should resolve the issue with the buggy function.