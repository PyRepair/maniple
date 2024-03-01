### Bug Explanation
The bug is caused by the inconsistent logic in determining the key_type of the input key. The key_type is incorrectly set to `'string'` regardless of the actual type of the key, leading to incorrect behavior in the following conditional statements.

### Bug Fix Strategy
1. Correctly determine the key_type based on the type of the key input.
2. Ensure that the key_type is properly set to `'integer'` or `'boolean'` for further processing.

### Corrected Function
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

    if isinstance(key, Index):
        key_type = key.inferred_type
    elif is_integer(key) or is_bool(key):
        key_type = 'integer'
    else:
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

This corrected version includes the necessary checks to properly determine the key_type based on the type of the key input, ensuring correct behavior throughout the function.