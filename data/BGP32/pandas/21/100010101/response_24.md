The bug in the `_get_with` function is that it does not handle the case when the key is a list or ndarray of strings properly. Instead of treating them as label-based indexing, it incorrectly tries to infer the key_type as "integer" which leads to the KeyError in the failing test cases.

To fix this bug, we need to specifically handle the case when the key is a list or ndarray of strings correctly.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determin if this slice is positional
        # or label based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray)) and key_type != 'integer':
        return self.loc[key]

    return self.reindex(key)
```

This corrected version properly handles the case when the key is a list or ndarray of strings by using label-based indexing (`self.loc[key]`). This fix ensures that the function behaves correctly according to the expected input/output values provided for the failing test cases.