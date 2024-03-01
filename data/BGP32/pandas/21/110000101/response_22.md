The bug in the `_get_with` function is in the code block where it checks the type of the `key`. The function incorrectly handles the case where `key` is a list-like object and tries to convert it to a list even when it is already one, resulting in unexpected behavior.

To fix the bug, we need to remove the unnecessary conversion of `key` to a list when it is already a list-like object. We can also simplify the code by directly checking for list-like objects instead of specific types like `np.ndarray` or `ExtensionArray`.

Here is the corrected version of the `_get_with` function:

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

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

This corrected version of the function should now properly handle all cases and return the expected values according to the provided test cases.