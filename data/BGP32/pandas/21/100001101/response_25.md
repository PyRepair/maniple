### Bug Explanation
The bug in the function `_get_with` arises from the case where the `key` variable is a scalar type (like a string) and the `key_type` is incorrectly inferred as `'string'` instead of `'integer'`. This causes the function to try to index the Series `self` using `self.loc[key]`, resulting in an error when the key is not found in the index.

### Bug Fix Strategy
To fix the bug, we need to correctly infer the type of the `key` variable as an integer when it is a scalar (like a string). This will ensure that the appropriate indexing method (`iloc` or `loc`) is used based on the type of the key.

### Corrected Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
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

    elif not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Note: The key_type == "boolean" case should be caught by the
    #  com.is_bool_indexer check in __getitem__
    if key_type == "integer" or key_type == "string":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

By updating the condition to consider `'string'` as a valid type for key, we can handle cases where the key could be a scalar like a string. This will resolve the bug and ensure correct indexing based on the type of the key passed to `_get_with` function.