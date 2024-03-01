### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the key types. The function wrongly assumes that the key type is always 'integer' when it could be a string or other types. This assumption leads to unexpected behavior and errors when non-integer keys are used.

### Bug Fix Strategy
To address this bug, we need to modify the logic to correctly identify and handle different key types such as strings, lists, or arrays. We should also ensure that the function can handle a wider range of key types to avoid the errors encountered in the failing test cases.

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

    if is_scalar(key) or not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
    else:
        key = [key]  # convert to list

    # Note: The key_type == "boolean" case should be caught by the
    #  com.is_bool_indexer check in __getitem__
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version of the `_get_with` function improves the handling of different types of keys, such as scalars, lists, strings, and arrays. It correctly identifies the key type and routes the execution based on the type of key being used, thus fixing the bug and ensuring the function behaves as expected for various input scenarios.