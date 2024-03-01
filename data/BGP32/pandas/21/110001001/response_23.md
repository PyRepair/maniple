The bug in the function `_get_with` arises due to the incorrect handling of the key type, leading to unexpected behavior based on the type of key provided. The key type is determined using `lib.infer_dtype(key, skipna=False)`, which may not always correctly identify the type of key.

To fix the bug, we can modify the function to correctly identify the key type and handle each type appropriately. We can simplify the logic by directly checking the type of the key and performing the necessary actions based on the type.

Here's the corrected version of the function:

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
        
        if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
            return self.reindex(key)
        
        if is_scalar(key):
            return self.loc[key]
        elif is_list_like(key):
            # handle the dup indexing case GH#4246
            return self.loc[key]
        
        raise TypeError(
            "Unsupported key type for indexing the Series"
        )
```

This corrected version directly handles the key types and eliminates the need for inferring the key type. The function now checks if the key is a slice, DataFrame, tuple, list-like, scalar, or else raises a `TypeError` for unsupported key types. This ensures that the function behaves correctly based on the type of key provided.