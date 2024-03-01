### Bug Explanation:
The bug occurs because the function `_get_with` is not properly handling the case when the key is a list-like object (such as a Series, ndarray, or Index) with string values. This leads to the key type being incorrectly inferred as "integer" when it should be "string", causing the function to return the wrong result or raise an error.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic in the `_get_with` function to correctly handle the case when the key is list-like with string values. We should ensure that the key type is correctly inferred as "string" in this case and then proceed with the appropriate indexing method (loc or iloc) based on the index type and whether positional indexing should be used.

### Corrected Version of the Function:
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

    key = ensure_index(key)
    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "string":
        return self.loc[key]

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

By ensuring that the key is converted to a valid index before inferring its type and then properly handling the "string" type case, the corrected function should now work as expected and pass the failing test cases.