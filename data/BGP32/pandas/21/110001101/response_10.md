### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the key type, which leads to the `key_type` being detected as `'string'` in all cases. This stems from the incorrect checking of key types and inferring the type using `lib.infer_dtype(key, skipna=False)`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the key type detection is accurate and aligns with the expected types. We can achieve this by revisiting the key type identification logic and ensuring that it correctly identifies the types of keys being passed.

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

    if is_scalar(key):
        return self.loc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
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

In the corrected version of the function, the logic for determining the key type has been adjusted to correctly handle scalars and improve the inference of the key type when dealing with different types of keys. This fix should address the issue of incorrect key type detection and ensure the function works as expected in all scenarios.