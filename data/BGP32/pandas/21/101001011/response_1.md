### Bug Explanation:
The bug occurs in the `_get_with` function when dealing with different types of indexers. Specifically, when `key` is not recognized as an array-like indexer, it falls back to treating it as a normal index, leading to incorrect behavior. This is evident in the provided runtime values where the `key_type` variable erroneously gets assigned the value `'string'` instead of the correct type.

### Bug Fix Strategy:
To fix the bug, we need to handle the cases where the `key` is not an array-like indexer appropriately. This involves distinguishing between different types of indexers and handling them accordingly to prevent falling back to default index behavior.

### Corrected Version of the Function:
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
    
    elif is_scalar(key):
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type in ["integer", "boolean"]:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if isinstance(key, list):
        return self.loc[key]
    
    return self.reindex(key)
```

### Changes Made:
1. Added a check for scalar keys using the `is_scalar` function to handle cases where the key is a single value.
2. Updated the condition for `key_type` to include handling boolean indexer as well.
3. Adjusted the logic to appropriately select `loc` or `iloc` based on the key type.
4. Made the function more robust to handle different types of indexers correctly.

By making these changes, the corrected `_get_with` function should now address the bug and provide consistent and accurate indexing behavior across different key types.