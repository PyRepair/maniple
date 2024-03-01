The bug in the provided `_get_with` function is located in the incorrect handling of the `key_type` variable. The function incorrectly infers the type of the key as `'integer'` in all cases other than when the key is a list. This leads to incorrect behavior when the key is of type `'string'` as seen in the expected cases.

To fix this bug, we should update the logic of determining the `key_type` based on the type of the key provided. We should also handle the case where the key is a list, as it needs a special treatment according to the expected cases.

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

    if is_list_like(key):
        if isinstance(key, Index):
            key_type = key.inferred_type
            key = key.to_list()
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

This corrected function should now properly handle the different cases as described in the expected values for each case. This fix ensures that the `key_type` is inferred correctly based on the type of the key being passed to the function.