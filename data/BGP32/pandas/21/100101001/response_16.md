The bug in the `_get_with` function arises from the incorrect handling of keys that are expected to raise a `KeyError` when accessing the Series. The function tries to infer the `key_type` based on the input key, but in the cases provided, the keys are not present in the Series index, leading to the incorrect `key_type` being identified as `'string'`.

To fix this bug, we need to handle the case where the key is not found in the Series index properly and raise a `KeyError` in those cases.

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

    if isinstance(key, list):
        return self.loc[key]

    # Handle the case where key is not found in the Series index
    if not any(self.index == k for k in key):
        raise KeyError(f"None of {key} are in the index")

    return self.reindex(key)
```

This corrected version adds a check to make sure that at least one key in the `key` list matches an index value before trying to access the Series using that key. If none of the keys are found in the index, it raises a `KeyError` with a relevant message.

This correction should resolve the failing test cases where the function currently returns with an incorrect `key_type` of `'string'`.