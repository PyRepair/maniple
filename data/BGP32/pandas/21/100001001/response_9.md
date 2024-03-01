To fix the bug in the provided function `_get_with`, we need to modify the logic for handling the key types. The issue seems to be with the identification of the key type, as indicated by the incorrect `key_type` variable values in all the runtime cases.

Based on the provided runtime values and types of variables, it is clear that the current method for inferring the key type is not functioning correctly, as it always returns `'string'` regardless of the actual key type.

To address this issue, we can simplify the key type detection by checking the type of the key directly instead of using the `infer_dtype` function. It seems that the key can either be a list, numpy array, ExtensionArray, Series, or Index. By directly checking these types, we can accurately determine how to handle the key for indexing.

### Corrected Version of the Function `_get_with`

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

    elif not is_list_like(key):
        return self.loc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = type(key).__name__.lower()

        if key_type == 'int32' or key_type == 'int64':
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
    
        elif key_type == 'list':
            return self.loc[key]
    
    return self.reindex(key)
```

In this corrected version, we directly check the type of the key and handle it accordingly. We also differentiate between integer key types and list key types to ensure the correct indexing method is used (`.loc` or `.iloc`). This approach should address the bug and handle different types of keys properly.