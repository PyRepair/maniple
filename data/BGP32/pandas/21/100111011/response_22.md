### Analysis:
The buggy function `_get_with` is designed to handle different types of inputs for indexing a Series. The failing test cases are focused on indexers like lists, ndarrays, Index, and Series, showcasing inconsistent behavior.

### Bug cause:
The bug occurs due to inconsistent handling of different indexer types in the `_get_with` function. Specifically, the function does not properly handle the case when a list-like indexer is provided, resulting in a KeyError when trying to index the Series.

### Bug Fix Strategy:
To fix the bug, we need to ensure consistent handling of different indexer types in the `_get_with` function. We should update the logic to handle list-like indexers correctly to align with the expected behavior. By doing so, we can resolve the KeyError issue reported in the failing tests.

### Corrected Version of the Function:
Here's the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, (list, np.ndarray)):
        return self._get_values_tuple(key)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
        
    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

### Explanation:
- The updated function now correctly handles list-like indexers by calling `_get_values_tuple` for these cases.
- The logic has been adjusted to ensure consistent behavior across different indexer types, addressing the reported KeyError issue.
- With this correction, the function should be able to pass the failing tests and provide the expected results.