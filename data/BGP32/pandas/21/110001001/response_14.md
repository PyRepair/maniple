The bug in the `_get_with` function lies in the logic to determine the `key_type`. The function incorrectly infers the key type as `'string'` in all cases, which leads to incorrect indexing decisions.

To fix this bug:
1. Check if the `key` variable is an instance of `Index` before inferring the key type.
2. If the `key` variable is an instance of `Index`, set the `key_type` as `key.inferred_type`.
3. If the `key` variable is not an instance of `Index`, infer the key type using `lib.infer_dtype(key, skipna=False)`.
4. Update the conditional logic based on the correct `key_type` to make appropriate indexing decisions.

Here is a corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determin if this slice is positional
        #  or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Note: The key_type == "boolean" case should be caught by the
    #  com.is_bool_indexer check in __getitem__
    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        #  (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

This corrected version should address the bug by correctly inferring the key type based on the input `key`, allowing for proper indexing decisions in the Series class.