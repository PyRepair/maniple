## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key` parameter when it is a list of strings. The function is supposed to determine the type of the key based on its contents and route the logic accordingly, but it fails to properly identify a list of strings as a valid type.

When `key` is a list of strings, the function incorrectly assumes it is not list-like and tries to access the value using `self.loc[key]`, which leads to a key error.

## Fix Strategy
To fix this bug, we need to address the logic that determines the type of the key parameter. Specifically, we need to properly handle the case where `key` is a list of strings by identifying it as a list-like object.

## Corrected Version

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

    # Properly handle list-like objects including a list of strings
    if is_list_like(key):
        return self.loc[key]

    if isinstance(key, (np.ndarray, ExtensionArray, Series, Index)):
        return self.loc[key]

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

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```