### Bug Explanation
The bug in the `_get_with` function is caused by the incorrect handling of the key parameter passed to it. The function is expecting different types of keys like a slice, a DataFrame, a tuple, or a list-like object, but the handling for these cases is not comprehensive. The bug arises when the key is a list, an ndarray, an Index, or a Series, where the function should be treating it differently based on its type.

### Bug Fix Strategy
To fix the bug, we need to properly handle the different types of keys that can be passed to the function. We should check the type of the key and then appropriately process it according to its type.

### Corrected Function
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

    if is_list_like(key):
        key = list(key)
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        key_type = lib.infer_dtype([key], skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type

    if key_type == "string":
        return self.reindex(key)
    else:
        raise KeyError(f"None of {key} are in the index")
```

### Changes Made
1. Check if the key is list-like using `is_list_like` function.
2. If the key is list-like, convert it to a list and infer its dtype.
3. Handle the case where the key type is 'string' and directly reindex.
4. Raise a KeyError if the key is not present in the index for any other dtype.