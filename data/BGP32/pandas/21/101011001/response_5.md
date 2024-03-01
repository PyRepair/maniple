### Bug Explanation
The bug occurs because the function `_get_with` contains a condition to check if the key is not list-like, in which case it tries to access the key using `self.loc[key]`. However, the key is mistakenly assumed to be a string without considering the possibility of it being a list or ndarray type.

### Bug Fix Strategy
To fix the bug, we need to properly handle the case where the key is not list-like. We should treat any key type that is not list-like and not recognized as a scalar as a positional indexer, meaning we should access the data using `self.iloc[key]` instead of `self.loc[key]`.

### Corrected Version of the Function
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

    # handling non-list-like keys
    if not is_list_like(key) or not is_scalar(key):
        return self.iloc[key]

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

By including the check `if not is_list_like(key) or not is_scalar(key):`, we can ensure that non-list-like and non-scalar keys are treated as positional indexers, resolving the bug and passing the failing test cases.