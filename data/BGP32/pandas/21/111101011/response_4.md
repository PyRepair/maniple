## Bug Explanation
The bug occurs in the `_get_with` function of the `Series` class when handling a list-like key that doesn't match any values in the index. In such cases, the function correctly raises a `KeyError` when using an ndarray, Index, or Series key, but does not raise the error and tries to proceed with a reindex operation when using a list key.

The root cause of the bug is the different treatment of list indexers compared to array-like indexers in the `_get_with` function. This inconsistency leads to unexpected behavior when a list key with no matches in the index is provided, causing incorrect handling and potentially undesired results.

## Fix Strategy
To fix the bug, we need to ensure that the `_get_with` function handles list-like keys consistently with array-like keys when there are no matches in the index. Specifically, we should update the code to raise a KeyError when a list key is provided and none of its elements match any values in the index.

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
    
    elif not is_list_like(key):
        return self.loc[key]
    
    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)
    
    if key_type == "integer":
        if not self.index.is_boolean():
            return self.loc[key]
        else:
            return self.iloc[key]
    
    if isinstance(key, list):
        if all(idx in self.index for idx in key):
            return self.loc[key]
        else:
            raise KeyError(f"None of {key} are in the index")
    
    return self.reindex(key)
```

By updating the handling of list keys in the `_get_with` function, the corrected version addresses the bug by consistently raising a KeyError when there are no matches in the Series index for the provided list-like key. This fix ensures uniform behavior across different types of indexers and resolves the inconsistency highlighted in the GitHub issue.