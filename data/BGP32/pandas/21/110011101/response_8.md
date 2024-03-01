### Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of the `key_type` variable, which is used to determine the type of the key being passed to the function. In the current implementation, the `key_type` is inferred using the `lib.infer_dtype` function, which sometimes leads to incorrect inference, causing the function to take the wrong path in determining how to process the key.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `key_type` is accurately determined based on the type of the key being passed. Instead of relying solely on the `lib.infer_dtype` function, we can use explicit checks on the type of the key to correctly identify whether to treat it as an integer, boolean, or others.

### Corrected Version of the Function
Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    
    if isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if is_scalar(key) and key not in self.index:
        raise KeyError(f"{key} not in index")
    
    if is_bool(key):
        return self._get_values_tuple(key)
    
    if is_integer(key):
        return self._get_values(key)
    
    if is_list_like(key):
        return self.loc[key]
    
    return self.reindex(key)
```

With this fix, the function will correctly determine the type of the key being passed and handle it accordingly, addressing the bug causing the failing tests.