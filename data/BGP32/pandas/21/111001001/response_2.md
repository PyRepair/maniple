The bug in the `_get_with` function arises due to the incorrect handling of the `key_type` variable, which is incorrectly inferred as `'string'` in all cases. The issue lies in the way the `key` variable is processed and the type of the `key` variable in different scenarios.

To fix the bug, we should update the logic for determining the `key_type`. We can modify the inference logic based on the type of the `key` variable provided. Below is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)  # Infer the type based on the key variable

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By updating the inference of `key_type` based on the type of the `key` variable provided, we ensure that the function correctly handles different types of keys and returns the expected result.

This correction addresses the issue of determining the correct `key_type` and allows the function to operate as intended based on the type of input keys.