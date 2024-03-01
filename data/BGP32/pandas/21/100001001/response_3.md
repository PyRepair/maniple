The issue in the provided `_get_with` function seems to be that the key_type is being incorrectly inferred as `'string'` for all input types, which causes incorrect branching logic. The function does not handle string type correctly in the branching conditions.

To fix this issue, we need to update the logic to correctly identify the type of the input `key` variable and adjust the branching conditions accordingly.

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

    if is_scalar(key):
        return self.loc[key]

    if is_list_like(key):
        key = list(key)

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

    raise TypeError("Unsupported key type for indexing")
```

This corrected version ensures that the key type is correctly identified prior to branching and provides the appropriate handling for different types of keys.