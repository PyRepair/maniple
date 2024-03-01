### Analysis:
The `def _get_with(self, key)` function is supposed to handle different types of input keys for pandas Series. However, there is a bug in the code that causes the function to fail when using a list as the key input, as observed in the failing test `test_getitem_no_matches`.

The failing test expects a `KeyError` exception to be raised when trying to access a non-existent key, but the function does not handle list-like keys properly, leading to the failure.

Based on the expected input and output values, the function should identify the `key_type` correctly and then use either `self.loc[key]` or `self.reindex(key)` based on the key type.

### Bug Explanation:
The bug arises from the incorrect handling of list-like keys in the `key` parameter. When a key is passed as a list, the function does not appropriately distinguish its type and fails to handle the case where the key does not exist in the index, leading to inconsistent behavior and raising a `KeyError`.

### Fix Strategy:
1. Identify the key type correctly and ensure it's processed accordingly.
2. Adjust the logic to handle list-like keys appropriately, distinguishing between accessing existing keys (`self.loc[key]`) and keys reindexing (`self.reindex(key)`).

### Corrected Function:

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

    elif not is_list_like(key):
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

    # Handle list-like keys and reindex appropriately
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series)):
        if len(set(key).intersection(self.index)):
            return self.loc[key]
        else:
            raise KeyError(f"None of {key} are in the index")

    return self.reindex(key)
```

By updating the logic above, the function should now correctly handle list-like keys and behave consistently with the expected input/output values, resolving the issue described on GitHub.