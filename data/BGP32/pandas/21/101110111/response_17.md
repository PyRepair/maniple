## Bug Analysis
1. The buggy function `_get_with` is trying to handle different types of indexers such as slices, dataframes, tuples, scalars, lists, numpy arrays, etc.
2. The failing test `test_getitem_no_matches` is using different types of indexers (`list`, `numpy array`, `pd.Index`, `pd.Series`) to index a `Series`.
3. The error message indicates that the function is not raising the expected `KeyError` when indexing with a `list`.
4. The expected input and output values for the failing test cases are provided, showing that the function should handle the indexers correctly to avoid the `KeyError`.

## Bug Explanation
The bug occurs because the `_get_with` function does not properly handle indexing with a `list` type as an indexer. The condition for non-list-like indexers is triggering the `fall back to position-based indexing` section in the code, leading to incorrect behavior.

## Bug Fix Strategy
To fix the bug:
1. Ensure that the function correctly handles indexing with a `list` type as an indexer.
2. Update the logic to properly differentiate between different types of indexers and handle them appropriately.
3. Make sure the function raises a `KeyError` when needed for indexing with unavailable values.

## Corrected Function
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    elif is_scalar(key):
        try:
            return self.loc[key]
        except KeyError:
            raise KeyError(f"None of [{key}] are in the index")
    
    elif isinstance(key, (list, np.ndarray, ExtensionArray)):
        key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        elif key_type == "string":
            # check for string-type indexers
            try:
                return self.loc[key]
            except KeyError:
                raise KeyError(f"None of [{key}] are in the index")
        
        elif key_type == "datetime":
            # handle datetime-type indexers
            try:
                return self.loc[key]
            except KeyError:
                raise KeyError(f"None of [{key}] are in the index")
        
        else:
            raise KeyError(f"None of [{key}] are in the index")
    
    elif isinstance(key, Index):
        key_type = key.inferred_type
        
        if key_type == "string":
            try:
                return self.loc[key]
            except KeyError:
                raise KeyError(f"None of [{key}] are in the index")
        
    return self.reindex(key)
```

By updating the logic within the `_get_with` function and handling different types of indexers properly, the corrected version of the function should now pass the failing test cases and resolve the issue reported on GitHub.