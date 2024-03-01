### Bug Analysis
1. The bug occurs when attempting to unstack a DataFrame with MultiIndex columns using a tuple as the level parameter.
2. The issue arises from the _get_level_number method in the MultiIndex class, which expects the level parameter to be an integer representing the level index, not a tuple of names.
3. The error message indicates that the method tries to find 'A' as an integer index within the list of names, resulting in a KeyError.
4. The bug originates in the _unstack_multiple function where it tries to convert the tuple of names passed as the level parameter into level numbers using _get_level_number.
  
### Bug Fix Strategy
1. The fix involves updating the _unstack_multiple function to handle the tuple of names correctly:
    - If the data is a Series, directly use the level parameter and handle the unstacking appropriately.
    - If the data is a DataFrame:
        - Check if the column names are in MultiIndex format.
        - Iterate through the levels in the tuple, converting the names into level numbers for unstacking.
2. By addressing the conversion from level names to level numbers correctly, the bug can be resolved.

### Corrected Function
```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    index = data.index

    if isinstance(data.index, MultiIndex):
        if isinstance(data, Series):
            dummy = data.copy()
            dummy.index = Index(get_compressed_ids(index), name="__placeholder__")
            return dummy.unstack("__placeholder__", fill_value=fill_value)
        
        if isinstance(data.columns, MultiIndex):
            result = data.copy()
            for loc in clocs:
                result = result.unstack(loc, fill_value=fill_value)
            return result

        for i, loc in enumerate(clocs):
            loc_num = index.get_loc_level(loc)
            if i == (len(clocs) - 1):
                dummy_index = Index(get_compressed_ids(loc), name="__placeholder__")
                dummy = data.copy()
                dummy.index = dummy_index
                return dummy.unstack("__placeholder__", fill_value=fill_value)
            else:
                data = data.unstack(loc_num, fill_value=fill_value)
        
    return data
```

By updating the _unstack_multiple function as shown above, the bug related to unstacking MultiIndex columns with tuples as level names should be fixed.