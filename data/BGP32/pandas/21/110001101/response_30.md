## Bug Explanation
The bug in the `_get_with` function lies in the incorrect handling of the key_type when the key is not recognized as a list-like object. In the current implementation, even if the key is a scalar that is not recognized as list-like, it tries to access the `loc` attribute of `self` without checking if it's a valid key for indexing.

## Bug Fix Strategy
To fix the bug, we need to update the handling of non-list-like keys. We should first check if the key is a valid indexer for the Series before attempting to access its location using `loc`. If the key is not suitable for indexing, we need to raise an appropriate error message.

## Corrected Version of the Function
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

    if not is_list_like(key) and not isinstance(key, (int, np.integer)):
        raise ValueError("Data type not supported for indexing")

    key = list(key)

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

    # handle the dup indexing case GH#4246
    return self.loc[key]
```

This corrected version of the function ensures that the key is only used for indexing if it is a valid index or integer. If it is not suitable for indexing, a ValueError is raised. Additionally, it maintains the handling of different key types based on their inferred data type.