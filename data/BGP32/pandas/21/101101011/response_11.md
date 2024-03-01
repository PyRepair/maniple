### Bug Fix Strategy:
The bug seems to originate from the inconsistency in how different types of indexers are handled within the `_get_with` function, especially when using a list as an indexer. The failing test cases indicate that the behavior is inconsistent for list, ndarray, Index, and Series indexers.

To fix the bug, we need to ensure consistent handling of all types of indexers, specifically when a list indexer is provided. We should aim to handle list indexers similarly to how other types of indexers are treated.

### Updated Corrected Version of the Function:
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, (ABCDataFrame, Index)):
        raise TypeError(
            "Indexing a Series with DataFrame or Index is not supported, use the appropriate DataFrame column or Series/index"
        )
    
    if isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if is_scalar(key):
        if key not in self.index:
            raise KeyError(f"{key} not in index")
        return self.loc[key]
    
    if isinstance(key, np.ndarray):
        key = key.tolist()

    if isinstance(key, (Index, list, Series)):
        return self.loc[key]

    return self.reindex(key)
```

### Explanation:
- Removed the check for `is_list_like`, as the key is being directly checked as scalar next.
- Added specific handling for scalar keys to check if the key is in the index and raise `KeyError` if not.
- Convert ndarray indexers to list to ensure consistency in handling.
- Added a check for `Index`, `list`, or `Series` types to directly return `self.loc[key]`.
- Updated the error message for DataFrame and Index inputs to be more informative.
- Updated the return statements for better flow control based on the type of indexer.

This corrected version ensures consistent handling of different types of indexers within the `_get_with` function.