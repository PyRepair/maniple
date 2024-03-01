## Bug Explanation
The bug in the `_get_with` function occurs when determining the `key_type` based on the input `key`. The function wrongly infers the key_type as `"integer"` when the key is a string (due to the incorrect `isinstance(key, list)` check before the key_type inference section). This results in the function taking the `else` path and trying to decide between positional or label-based indexing, which is incorrect behavior for string keys.

## Fix Strategy
To fix the bug, we need to correct the check for string keys before inferring the key_type. We should first identify strings and proceed accordingly. This fix will ensure that the key_type inference logic proceeds correctly for string keys.

## Corrected Function
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
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar, GH#32684
        return self.loc[key]

    key = ensure_index(key)

    if key.inferred_type == "string":
        return self.loc[key]

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

By modifying the corrected function as mentioned, the bug in key type inference is fixed, and the function should work correctly for the provided test cases as expected.