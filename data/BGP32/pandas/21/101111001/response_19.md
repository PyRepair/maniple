### Bug Analysis:
The bug in the `_get_with` function arises from the incorrect check for the key_type. The function erroneously assigns `'string'` as the `key_type` in all cases, which leads to the wrong execution path in handling the key. This discrepancy causes the KeyError to not be raised as expected in the test cases.

### Bug Explanation:
The `_get_with` function wrongly determines the `key_type` to be `'string'` for all cases of keys, regardless of their actual type. This generic assignment causes the function to take the wrong execution path, leading to incorrect handling of the key and failing to raise the KeyError as expected in the test.

### Bug Fix:
To fix the bug, we need to accurately infer the data type of the key. By correctly determining the `key_type` based on the key's actual type, we can ensure that the function follows the correct path for processing the key.

### Corrected Version of the `_get_with` function:
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

    # Infer the key type correctly
    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    elif isinstance(key, list):
        return self.loc[key]
    
    return self.reindex(key)
```

By correcting the key type inference mechanism in the `_get_with` function, the function should now handle the keys properly and resolve the issue with the failing test cases.