### Bug Explanation
The bug is caused by the function `_get_with(self, key)` not handling the case where the key is a `list`, `ndarray`, `Index`, or `Series`. The function incorrectly infers the `key_type` as "integer" and does not handle the case where `key_type` is "string".

### Bug Fix Strategy
1. Check the type of the key at the beginning of the function.
2. If the key is not a list-like object, handle it appropriately.
3. Update the function to correctly infer the type of the key and handle different key types accordingly.

### Corrected Code

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

    # Handle list, ndarray, Index, Series
    key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if key_type == "string":
        return self.loc[key]

    if isinstance(key, (list, Index)):
        return self.loc[key]

    return self.reindex(key)
``` 

By updating the function as shown above, the bug should be fixed, and the failing tests should pass.