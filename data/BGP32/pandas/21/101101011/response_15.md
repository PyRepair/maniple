The bug in the `_get_with` function arises from the handling of different types of indexers, specifically when a list indexer is used. The current implementation treats list indexers differently from other array-like indexers, leading to inconsistent behavior. This discrepancy is highlighted by the failing test cases, which expect consistent behavior across different indexer types.

To fix this issue, we need to ensure that list indexers are handled in a consistent manner with other array-like indexers. We can simplify the logic within the function to handle all indexers uniformly, which will align with the expected behavior in the failing tests.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    # Handle all indexers uniformly
    key_array = np.asarray(key)
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key_array, skipna=False)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    return self.reindex(key_array)
```

This revised implementation ensures that all indexer types, including lists, are treated in a consistent and appropriate manner. It aligns with the expected behavior in the failing test cases and resolves the inconsistency highlighted in the GitHub issue.

By updating the `_get_with` function with the above corrected version, the issue reported on GitHub should be addressed, and the failing test cases should pass as expected.