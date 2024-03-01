The bug in the `_get_with` function stems from the incorrect handling of the key type. The function wrongly assumes the key type is "integer" when it is actually "string". This leads to the wrong path being taken in the conditional statement and results in incorrect behavior.

To fix this bug, we need to adjust the logic to correctly identify the key type as "string" and handle it accordingly.

Here is the corrected version of the `_get_with` function:

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

    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "string":
        return self.loc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        return self.loc[key]
    
    return self.reindex(key)
```

With this correction, the function will correctly handle cases where the key type is "string" and follow the appropriate path for indexing. This should resolve the bug and make the function work as expected for the failing tests.