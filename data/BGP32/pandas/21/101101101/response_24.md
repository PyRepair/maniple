### Bug Explanation
The bug in the `_get_with` function arises from incorrectly inferring the data type (`key_type`) of the input `key` variable. In the provided cases, the `key_type` is being set to `'string'` for all cases, regardless of the actual data type of the `key` input. This incorrect inference leads to incorrect branching in the function logic, causing the function to return the wrong outputs in some scenarios.

### Bug Fix Strategy
To fix the bug, we need to ensure that the data type inference for the `key` variable is correct. We should accurately determine whether the `key` is an integer index, a list, an ndarray, an ExtensionArray, a Series, or an Index, and set the `key_type` accordingly. This will enable the function to correctly handle different types of input keys and return the expected results.

### Corrected Function
Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, pd.DataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif not is_list_like(key):
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, list):
            return self.loc[key]
        return self.reindex(key)
    
    return self.reindex(key)
```

By correctly inferring the data type of the `key` variable based on its actual type and incorporating suitable conditionals for different types of keys, the corrected function should now return the expected results for the failing test cases.