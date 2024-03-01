The bug in the `_get_with` function is likely due to the incorrect handling of the key type in the case where `key` is not a list-like object. The code snippet that converts `key` to a list if it's not already a list-like object might be causing unexpected behavior.

To fix this bug, you should modify the function to correctly handle the case where `key` is not list-like and ensure that the key type is appropriately determined.

Here is a corrected version of the `_get_with` function:

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
        key = [key]  # Convert scalar to list

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    key_type = lib.infer_dtype(key)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This correction ensures that scalars are correctly converted to lists and that the key type is inferred properly for further processing. This should address the issue seen in the failing tests.