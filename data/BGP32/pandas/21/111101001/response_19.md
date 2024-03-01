The bug in the `_get_with` function seems to be related to the incorrect identification of the key type when the key is a list or an ndarray of non-numeric values. This leads to the function incorrectly inferring the key type as "integer" when it should be "string". As a result, the function tries to access the key as an index position rather than a label, which causes the KeyError in the failing test cases.

To fix this bug, we need to update the key type logic to correctly identify non-numeric keys as "string" instead of "integer". Here is the corrected version of the `_get_with` function:

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

    # Update the key type logic for lists and ndarrays of non-numeric values
    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "string":
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the `_get_with` function should now correctly handle non-numeric keys as labels and prevent the KeyError in the failing test cases.