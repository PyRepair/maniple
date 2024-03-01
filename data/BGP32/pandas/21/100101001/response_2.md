The issue in the `_get_with` function is that it wrongly infers the `key_type` as `'string'` for all input types in the provided test cases. This causes the function to take the wrong path in determining how to handle the key during indexing, resulting in a KeyError in the test cases.

To fix this bug, we need to correctly determine the `key_type` based on the input `key`. The bug arises from the incorrect handling of different input types and inferring a wrong type. We can address this by examining the type of the `key` input and setting the `key_type` accordingly.

Here's the corrected version of the `_get_with` function:

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

    elif not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        if isinstance(key, list):
            return self.loc[key]

        return self.reindex(key)
    else:
        return self.loc[key]
```

By correctly inferring the `key_type` and handling different input types appropriately, the corrected function should now pass the failing test cases.