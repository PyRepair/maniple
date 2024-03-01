The bug in the `_get_with` function arises from the incorrect handling of the `key_type` variable. The function currently sets `key_type` using the `lib.infer_dtype` function, which is causing issues when dealing with string-type keys. The `lib.infer_dtype` function is incorrectly inferring the key type as "integer" instead of "string", leading to the wrong path being chosen for indexing.

To fix this bug, we can modify the code to explicitly check if the key is of type "string" and handle it accordingly.

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
    
    elif isinstance(key, str):
        return self.loc[key]
    
    if not is_list_like(key):
        return self.loc[key]

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

This correction includes an explicit check for string-type `key`, leading to the correct path for indexing when dealing with string keys. This change should address the failing tests and ensure proper indexing behavior for the Series class.