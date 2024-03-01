## Bug Explanation

The bug occurs when attempting to index a Series using a list-like input (either a list, ndarray, Index, or Series) that contains no matching values in the Series index. The current implementation of the `_get_with` function treats different types of list-like input differently, leading to inconsistent behavior.

When using a list-like input that contains no matching values, except for a list input, the function should raise a `KeyError` with a specific message. However, for other types of list-like inputs such as ndarray, Index, or Series, the function does not raise the `KeyError` with the expected message.

The discrepancy between how different list-like inputs are handled causes the failing tests since the expectation is consistent behavior across all list-like types.

## Bug Fix Strategy

To fix the bug, we need to ensure that the `_get_with` function handles all types of list-like input (list, ndarray, Index, Series) uniformly when encountering a situation where no matching values are found in the Series index. This can be achieved by updating the conditional statements to follow the same flow for all list-like types.

## Corrected Function

Below is the corrected version of the `_get_with` function that addresses the bug.

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
    
        key = ensure_index(key)
    
        key_type = lib.infer_dtype(key, skipna=False)
    
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]

        key = ensure_index(key)

        if key.empty:
            raise KeyError(f"None of {key} are in the {self.index}")
        
        return self.loc[key]
```

In the corrected version, we ensure to convert all list-like inputs to Index using `ensure_index`. Additionally, when no matching values are found in the Series index, a `KeyError` is raised with the appropriate message for all list-like input types, ensuring uniform behavior.