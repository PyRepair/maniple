The bug in the `_get_with` function lies in the section where it determines the `key_type`. It incorrectly infers the dtype of the key as `'string'` in all cases, causing the subsequent logic to fail.

To fix this bug, we need to correctly infer the dtype of the key and handle each case accordingly. Below is the corrected version of the `_get_with` function:

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

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == 'boolean':
        key_type = 'boolean'

    if key_type in ['integer', 'string', 'mixed-integer']:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, Series)):
        return self.loc[key]

    return self.reindex(key)
```

This corrected version handles the key_type according to its inferred dtype. It ensures that the key_type is correctly identified before proceeding with the indexing operation.

By making these changes, the `_get_with` function should now pass the failing tests and behave correctly for the specified input cases.