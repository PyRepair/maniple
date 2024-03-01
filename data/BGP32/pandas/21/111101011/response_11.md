The bug in the `_get_with` function is causing inconsistent behavior when indexing a Series with different types of indexers, specifically when using a list indexer. This leads to a KeyError when trying to access values that do not match any existing index values.

The issue arises due to the handling of different types of indexers in the `_get_with` function. The function is expecting particular types such as `Index`, `np.ndarray`, `ExtensionArray`, `Series`, or `Index`, but it fails to handle list-like indexers correctly, resulting in the KeyError.

To fix this bug, we need to ensure that list-like indexers are correctly handled and that the appropriate KeyError is raised when needed. 

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
    
    elif not is_list_like(key):
        return self.loc[key]

    key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "boolean":
        return self.loc[key]

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]
    
    return self.reindex(key)
```

This corrected version includes handling for list-like indexers to ensure consistent behavior when indexing a Series with different types of indexers, as was expected in the failing test case. It should now pass the failing test and resolve the inconsistency reported in the GitHub issue.