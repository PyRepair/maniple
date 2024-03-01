The bug in the `_get_with` function is due to the incorrect handling of key types and the inconsistency in checking for valid key types. The function fails to properly differentiate between different key types, leading to a KeyError when trying to access non-existent keys in the Series index.

To fix this bug, we should update the key type checking logic and handle the case where the key is not found in the index properly. We should also ensure that key types are correctly inferred and processed.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, (ABCDataFrame, tuple)):
        return self.loc[key]
    
    if not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar
        return self.loc[key]

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

    # Handle the case where key is not found in the index
    missing_keys = set(key) - set(self.index)
    if missing_keys:
        raise KeyError(f"None of {missing_keys} are in the index")

    return self.reindex(key)
```

This corrected version will properly handle different key types, correctly infer key types, and raise a KeyError if keys are not found in the Series index, which fixes the failing test cases.