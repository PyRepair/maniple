The bug in the `_get_with` function is causing different behaviors for list indexers compared to array-like indexers when accessing a Series. This inconsistency is highlighted in the failing test `test_getitem_no_matches` where the error message indicates that the key provided is not found in the index.

Upon analyzing the function and the failing test, we can see that the key_type is inferred as `'string'` in all cases instead of the actual type of the key passed, which results in incorrect handling and indexing.

To fix this bug, we need to ensure that the `key_type` is correctly inferred based on the type of the key provided. The correction involves handling the cases where the key is a list or an ndarray by converting it into a list before processing.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
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

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key = list(key)  # Convert key to list
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By ensuring that the key is converted to a list before infering its type, we address the incorrect behavior highlighted in the failing test. The corrected function should now pass the failing test and resolve the issue reported on GitHub.