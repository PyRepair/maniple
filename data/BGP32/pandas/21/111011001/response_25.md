### Bug Analysis
- The bug occurs when trying to get items from a Series using a key that is not found in the index.
- The function `_get_with` checks the type of the key and takes different actions based on the type to get the values.
- The issue seems to be related to the handling of the key type in the function.
- The bug is triggered when the key is not found in the index, resulting in a `KeyError`.

### Bug Fix Strategy
- We need to ensure that the function handles cases where the key is not found in the index appropriately.
- The key should be checked against the index values before proceeding to extract values.
- If the key is not found in the index, the function should raise a `KeyError`.
- We also need to handle different types of keys more consistently to avoid errors.

### Corrected Code
```python
# Fixed version of the _get_with function
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

    if not self.index.isin(key).any():
        raise KeyError(f"None of {key} are in the index")

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By modifying the `_get_with` function to check if the key is present in the index using `isin(key)`, we can avoid the KeyError when the key is not found. This change ensures that the function handles missing keys gracefully and provides a more consistent behavior.