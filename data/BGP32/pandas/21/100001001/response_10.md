The issue in the `_get_with` function lies in the `key_type` assignment and subsequent conditional branches based on it. The incorrect handling of different key types leads to the function failing in all provided cases where the input keys are strings. The function mistakenly infers all keys as integers, which results in incorrect behavior when accessing the data.

To fix the bug:
- We should correctly determine the key type to differentiate between different types of keys (e.g., strings, integers).
- Update the conditional branches based on the key type to handle each key type appropriately.

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
    elif is_list_like(key) and not isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if hasattr(key, "inferred_type"):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    elif key_type == "string":
        return self.loc[key]
    else:
        return self.reindex(key)
```

This corrected version addresses the key type inference issue and appropriately handles keys based on their inferred type. Now the function should work correctly based on the identified bug scenarios.