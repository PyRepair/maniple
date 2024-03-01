The function `_get_with` is intended to handle different types of keys for indexing a Series object. However, there are several issues in the function that need to be addressed:

1. In the last part of the function where it checks for the type of the `key`, there is a conflicting check for `isinstance(key, list)` and `isinstance(key, Index)`, which can lead to unexpected behavior.
2. The logic for determining the `key_type` based on the type of the `key` variable seems inconsistent and may not work as expected.

To fix the bug, we can revise the function as follows:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key):
        return self.loc[key]

    # Convert key to list if it's not already one
    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = [key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "string":
        return self.reindex(key)

    elif key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

This revised version addresses the inconsistent type checks and ensures that the logic for determining `key_type` is correct based on the type of the `key`. This should now correctly handle the expected values and types for the provided test cases.