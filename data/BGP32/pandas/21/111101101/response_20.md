The bug in the `_get_with` function arises from the incorrect handling of the key variable when it contains non-list-like elements. This leads to the incorrect determination of the `key_type` and subsequent incorrect branching of the code based on the `key_type`.

To fix this bug, we need to ensure that the type checking and handling of the `key` variable is correct for all possible scenarios. Specifically, we should handle non-list-like keys properly to determine their type and perform the necessary operations accordingly.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    # Handle non-list-like keys properly
    if not is_list_like(key):
        key = [key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
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

This corrected version ensures proper handling of non-list-like keys and correctly determines the `key_type` for branching in the subsequent logic.

After applying this fix, the `_get_with` function should now pass the failing test cases provided.