The bug in the `_get_with` function is causing inconsistent behavior when using different types of indexers. Specifically, when passing a list indexer, the function fails to handle it properly, resulting in a `KeyError` exception. This behavior is not consistent with how other types of indexers are handled.

The issue originates from the `elif not is_list_like(key):` condition in the function, which wrongly falls back to `self.loc[key]` when dealing with a list indexer. This leads to incorrect handling and triggers the `KeyError`.

To fix the bug, we need to update the function to properly handle list-like indexers and ensure consistency across different indexer types.

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

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type in ("string", "unicode"):
        key = ensure_index(key)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This updated version includes proper handling for list-like indexers and ensures consistency in how different types of indexers are processed.

By incorporating these changes, the `_get_with` function should now pass the failing test cases, satisfy the expected input/output values, and resolve the issue reported in GitHub regarding inconsistent behavior with different indexers.