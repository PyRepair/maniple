The bug in the `_get_with` function arises from the implementation of handling different types of indexers, specifically when dealing with a list indexer. The function fails to properly handle list-like indexers, leading to a KeyError. 

The issue is related to how different types of indexers are processed and how the exception is handled for a list indexer. The failing test cases highlight the inconsistency in behavior when using different indexer types.

To fix this bug, we need to adjust the logic in the `_get_with` function to properly handle list-like indexers and ensure consistent behavior across different indexer types.

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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, List):
        return self.loc[key]

    if not isinstance(key, (Series, Index)):
        return self.reindex(key)

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
```

This corrected version of the function addresses the discrepancy in handling list-like indexers, ensuring that all types of indexers are processed consistently and avoiding the KeyError issue.

By making these changes, the `_get_with` function should now pass the failing test cases and resolve the reported issue on GitHub related to inconsistent behavior with different indexer types.