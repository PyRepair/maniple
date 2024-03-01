## Bug Explanation
The bug in the `_get_with` function arises due to the incorrect handling of different types of keys and the determination of the `key_type`. The function is designed to select values based on different types of keys, but in some cases, the key type is not correctly identified which leads to unexpected behavior.

1. In Case 1, if the key is a list of strings, the function incorrectly identifies the key type as `'string'`. This can cause issues when trying to access the values based on this key type.

2. In Cases 2 and 3, the function fails to correctly identify the key type when the key is an ndarray or an Index object, resulting in the same issue of an incorrect key type.

3. In Case 4, when the key is a Series object, the function handles it as a scalar key which again leads to incorrect key type determination.

## Bug Fix Strategy
To fix the bug, we need to revise the way the key type is identified in the function. We should ensure that the key type is correctly determined for various types of keys to avoid unexpected behaviors.

## Corrected Version of the Function
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

By removing the unnecessary checks and improving the key type determination logic, the corrected version of the `_get_with` function should now handle different types of keys correctly and avoid the previous bug.