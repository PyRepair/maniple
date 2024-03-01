### Bug Explanation
The bug in the `_get_with` function arises from the key_type being set to `'string'` in all cases, regardless of the actual type of the key. This leads to incorrect branch selections later in the function, causing the KeyError to not be raised as expected in the failing tests.

### Bug Fix Strategy
To fix the bug, we need to correctly infer the type of the `key` variable, ensuring that it reflects the actual type of the input `key`. This will enable proper handling of different key types and prevent the KeyError from not being raised.

### Corrected Version of the Function
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
    
    # Infer the correct key type
    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    
    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

By ensuring the correct inference of the key type, the corrected function should now handle different key types properly and raise the KeyError as expected in the failing tests.