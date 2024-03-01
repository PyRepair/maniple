### Analysis
1. The function `_unstack_multiple` deals with unstacking hierarchical data based on specified levels.
2. The function gets the index information from the provided data and manipulates it based on the `clocs` parameter.
3. The GitHub issue provides a failing test case where unstacking with a tuple name fails.
4. The bug occurs when trying to determine the level number from the tuple name causing `KeyError`.

### Bug Location and Cause
The bug occurs in the following line:
```python
clocs = [index._get_level_number(i) for i in clocs]
```
The `clocs` parameter when passed as a tuple fails to be recognized correctly resulting in a `KeyError`. This is caused by the function attempting to find the level number directly from the tuple name rather than handling it explicitly as a MultiIndex level.

### Strategy for Fixing the Bug
To fix the bug, the function needs to handle the case where `clocs` is a tuple representing MultiIndex levels differently from other scenarios. It should extract the necessary information from the tuple to identify the levels correctly.

### Corrected Function
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    if isinstance(clocs, tuple):
        clocs = [clocs]
    
    cloc_indices = [index.get_loc(level) if isinstance(level, tuple)
                    else index._get_level_number(level) for level in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in cloc_indices]

    ...
```

The revised section of the function correctly handles `clocs` when it's passed as a tuple and extracts the level information by checking the type of the level being passed. This fix will address the KeyError issue when unstacking with tuple names.