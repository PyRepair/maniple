### Bug Analysis:
The buggy function `_get_with` is failing to handle the case where the key is a list or ndarray that contains only one element. This triggers the conditional branch `elif not is_list_like(key)` which then tries to access the element within the Series using `self.loc[key]`. However, in this specific case, `key` is not a list-like object, but a single value, causing a `KeyError` to be raised.

### Bug Fix Strategy:
To fix the bug, we need to handle the case where `key` is not list-like separately. We can modify the condition to check the length of `key` and handle the single-element key appropriately.

### Corrected Version of the `_get_with` Function:
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

    if not is_list_like(key) or len(key) == 1:  # Handle single-item key separately
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

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

By implementing this fix, we handle the case where the key is not a list-like object separately and ensure that the single-element key is accessed correctly using `self.loc[key]`.