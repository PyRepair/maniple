The bug in the `_get_with` function lies in the incorrect handling of the key_type when it is a string. The current implementation assigns `key_type = 'integer'` if the key_type is a string, which is incorrect. This leads to the incorrect behavior and the failing tests.

To fix the bug, we need to update the condition checking for the key_type as a string and handle it correctly. We should check if the key_type is a string and then convert it to `object` type to properly handle it.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
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

    elif not is_list_like(key):
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

    if key_type == "string":
        key = np.asarray(key, dtype=object)

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This correction ensures that the key_type "string" is handled correctly by converting the key to an `object` type array to properly process it. This fix should make the function behave as expected and pass the failing tests.