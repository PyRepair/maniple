### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of string keys. The function fails to differentiate between different types of keys (list, ndarray, Index) and treats them all as strings, leading to unexpected behavior.

### Bug Fix Strategy
To fix the bug, we need to properly identify the type of the key passed to the function and handle each case accordingly. Specifically, when dealing with string keys, we should ensure that they are correctly processed without being treated as a different type.

### Corrected Version of the Function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        # or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif is_scalar(key) or is_list_like(key) or is_extension_array_dtype(key):
        key = ensure_index(key)

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = [key]

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray)):
        return self.loc[key]

    return self.reindex(key)
```

In the corrected version:
- We ensure that scalar, list-like, and extension array keys are transformed into an Index type for uniform handling.
- We properly identify the key type using `lib.infer_dtype` function and handle integer keys with position-based or label-based indexing.
- We correctly handle list and ndarray keys by using `loc` indexing.
- Finally, for other cases, we default to reindexing the key.