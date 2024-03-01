The issue in the `_get_with` function arises from the mishandling of the `key_type` variable, which is incorrectly inferred as `'string'` when it should be `'object'` due to the presence of strings in the key values.

To fix this bug, we need to ensure that the `key_type` is correctly inferred based on the actual data type of the key values. We can achieve this by modifying the code that infers the `key_type`.

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

    # Improved code to correctly infer the key_type based on the key values
    key_is_list_like = is_list_like(key)
    if not key_is_list_like:
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        # Check if any element is not of a scalar type
        scalar_elements = all(is_scalar(elem) for elem in key)
        if not scalar_elements:
            key_type = 'object'
        else:
            key_type = lib.infer_dtype(key, skipna=False)

    if key_type == 'integer':
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version includes a more robust check for inferring the `key_type` when handling different types of keys.

After applying this fix, the function should correctly handle keys containing strings like in the failing test cases.