The bug in the `_get_with` function lies in the incorrect handling of the `key_type` variable. The function wrongly determines the `key_type` as `'string'` regardless of the input key type, leading to the wrong path being taken in the subsequent conditional statements.

To fix this bug, we need to correctly infer the `key_type` based on the type of the `key` input. We can use the `lib.infer_dtype` function to accurately determine the type of the `key`, ensuring that the correct indexing method is used.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        # or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        # (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

This corrected version ensures the `key_type` is accurately determined and used to index the series correctly based on the input key type.

Please test this corrected version using the failing test cases provided to confirm the fix.