The bug in the `_get_with` function arises from incorrectly inferring the `key_type` when dealing with non-list-like keys, leading to an incorrect branch being taken in the function logic. The bug occurs when the `key` is not list-like and is a scalar value, leading to `lib.infer_dtype` incorrectly inferring the key type as `'string'`. This incorrect key type causes the function to take the wrong branch and results in a KeyError being raised in the failing test.

To fix this bug, we need to properly handle scalar values when inferring the key type. We should directly check if the key is a scalar value and handle it appropriately instead of relying on `lib.infer_dtype`. We can achieve this by checking if the key is a scalar and then directly attempting to access the key using label-based indexing (`self.loc[key]`).

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

    if not is_list_like(key) or is_scalar(key):
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

By checking if the key is a scalar value and handling it before inferring the key type, the corrected function should now properly handle the case of non-list-like keys and prevent the KeyError from being raised.