The bug in the `_get_with` function lies in the logic to handle various types of `key` inputs. The bug is causing an incorrect determination of the `key_type`, leading to the wrong branch being taken for indexing, resulting in a `KeyError`.

The issue arises when handling the case where `key` is not list-like. The function wrongly falls into the `return self.loc[key]` branch because it incorrectly identifies the `key_type` as `'string'`, which then triggers the wrong indexing method.

To fix the bug, we need to properly determine the `key_type` for non-list-like keys and select the appropriate indexing method based on that type.

Here is the corrected version of the `_get_with` function:

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

    # Handle non-list-like keys properly
    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type in ('string', 'mixed-integer', 'mixed-integer-float'):
        return self.loc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        elif isinstance(key, list):
            return self.loc[key]
    
    if key_type == 'integer':
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

This corrected version should properly handle different types of `key` inputs and select the appropriate indexing method accordingly. It should now pass the failing tests.