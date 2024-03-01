### Bug Explanation
The bug lies in how the function `_get_with` handles different types of indexers, specifically when dealing with a list-like indexer that doesn't match any values in the Series' index. The function incorrectly reindexes in this case instead of raising a `KeyError`.

When handling a list-like indexer that doesn't match any values in the Series' index, the function should raise a `KeyError` to maintain consistency with other indexer types. The GitHub issue discusses this inconsistency and suggests aligning the behavior of list indexers with array-like indexers.

### Bug Fix Strategy
To fix the bug, we should modify the function to raise a `KeyError` when dealing with a list-like indexer that doesn't match any values in the Series' index. This will align the behavior of list indexers with other indexers and resolve the inconsistency highlighted in the GitHub issue.

### Corrected Version of the Function
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
    
    if not is_list_like(key):
        return self.loc[key]
    
    if not any(value in self.index for value in key):
        raise KeyError(f"None of {key} are in the index")
    
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        return self.loc[key]
    
    return self.reindex(key)
```

By implementing this corrected version, the function will now raise a `KeyError` when a list-like indexer doesn't match any values in the Series' index, ensuring consistency with other indexer types.