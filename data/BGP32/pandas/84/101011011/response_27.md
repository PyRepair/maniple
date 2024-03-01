### Bug Explanation
The bug occurs because the function `_get_level_number` is expecting a level name as input, but it receives a tuple instead of a string level name. This leads to the error where it fails to find the tuple name in the list of level names.

### Bug Fix Strategy
To fix this bug, we need to ensure that the `clocs` variable receives only the level names, not tuples. To handle tuple names, we should first extract the level names from the tuple before passing them to the `_get_level_number` function.

### Corrected Function
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    # Extract level names from tuples, if needed
    clocs = [i if not isinstance(i, tuple) else i[0] for i in clocs]

    clocs = [index._get_level_number(i) for i in clocs]
    
    # The rest of the function remains unchanged
    # ...
```

After making the above correction, the function should now correctly handle both single-level and multi-level indices without causing errors related to unrecognized level names.