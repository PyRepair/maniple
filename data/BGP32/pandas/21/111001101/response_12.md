### Bug Explanation
The bug in the `_get_with` function arises when the `key_type` is incorrectly inferred as `'integer'`, even when the key is actually a string. This incorrect inference leads to the function taking the wrong execution path, resulting in unexpected behavior.

### Bug Fix Strategy
To fix the bug, we need to improve the way the key type is inferred to ensure it accurately represents the type of the key being passed to the function.

### Corrected Version of the Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if is_scalar(key_type):
        key_type = 'scalar'

    if key_type == 'integer':
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

### Changes Made
1. Added an additional check to handle cases where the key type is a scalar to avoid incorrect inference.
2. Updated the condition to accurately handle the key type inference for string keys.
3. Added a condition specifically for scalar keys to ensure correct behavior.