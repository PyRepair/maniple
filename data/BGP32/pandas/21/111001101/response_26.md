### Bug Explanation
The bug in the `_get_with` function arises from a mismatch between the way the `key_type` variable is inferred and how it is subsequently used to determine the indexing method (`iloc` or `loc`). The bug is specifically in the section where the variable `key_type` is determined. The function fails to properly identify the type of the key when it is a list, resulting in an incorrect inference of `'string'` for all cases.

### Bug Fix Strategy
To fix the bug, we need to correctly infer the type of the key when it is a list. We can utilize the `is_bool_indexer` function to determine if the key should be treated as boolean or not. This will allow us to correctly identify list-like keys and decide between positional (`iloc`) and label-based (`loc`) indexing.

### Corrected Version
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

    elif is_bool(key):
        return self.loc[key]

    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == 'integer' or (is_bool_indexer(key) and not self.index.is_object()):
            return self.iloc[key]
        else:
            return self.loc[key]

    else:
        return self.reindex(key)
``` 

This corrected version utilises the `is_bool_indexer` function to properly determine the type of the key when it is a list. This ensures that the correct indexing method (`iloc` or `loc`) is selected based on the key type.