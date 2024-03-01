### Bug Explanation
The bug in the `_get_with` function lies in the logic that determines the `key_type` when the `key` parameter is a list, np.ndarray, ExtensionArray, Series, or Index. The current implementation incorrectly infers the `key_type` as `'string'` for all these types of keys, which is causing the function to not handle the keys appropriately.

### Bug Fix Strategy
To fix the bug, we need to correctly determine the `key_type` based on the type of key being provided. We should handle different types of keys such as list, np.ndarray, ExtensionArray, Series, or Index separately to ensure proper indexing behavior.

### Corrected Version of the `_get_with` Function
Below is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # Determine if this slice is positional or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray)):
        key_type = lib.infer_dtype(key, skipna=False)
    elif isinstance(key, Series):
        key_type = key._data._inferred_type
    elif isinstance(key, Index):
        key_type = key.inferred_type

    if key_type in ["integer", "mixed-integer"]:
        # Determine whether to use positional or label-based indexing
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    # Handle the case where key is a list, Series, or Index
    if isinstance(key, (list, Series, Index)):
        return self.loc[key]

    return self.reindex(key)
```

By correctly inferring the `key_type` based on the type of the provided `key` and handling different key types appropriately, the corrected `_get_with` function should now pass the failing test cases.