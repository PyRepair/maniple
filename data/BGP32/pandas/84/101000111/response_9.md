### Analysis:
1. The function `_unstack_multiple` is designed to unstack data with multiple levels of indexing.
2. The bug seems to be related to the handling of tuple names passed as input for `clocs`.
3. The function is producing an error when attempting to process levels of indexing due to an issue with the input type and structure of the `clocs`.
4. The error message `KeyError: 'Level A not found'` indicates that the function is unable to locate the specified level in the MultiIndex.
   
### Bug Fix Strategy:
1. Ensure that the `clocs` input parameter is properly handled to extract the correct levels for unstacking.
2. Modify the function to correctly process the `clocs` input, especially when tuple names are used.
3. Correct the level extraction logic to match the expected input structure.

### Bug Fix Implementation:
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # Extract the levels containing names from a tuple
    index = data.index
    cloc_names = [(x if isinstance(x, str) else x[1]) for x in clocs]
    
    clocs = [index._get_level_number(i) for i in cloc_names]

    # The rest of the function remains the same
```

Following the fix, the function should be able to properly handle tuple names passed as input for `clocs` during the unstacking process.