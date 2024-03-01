The bug in the `_get_with` function is related to how different types of indexers are handled, resulting in inconsistent behavior between list indexers and other types of array-like indexers. The issue specifically arises when trying to access elements in a Series using a list indexer that contains no match to the Series index.

### Error Location:
The bug occurs in the section of code handling the different types of indexers. When a list indexer is used and it contains no match to the Series index, an error is raised due to the incorrect handling of the key type.

### Cause of the Bug:
1. The function checks if the key is list-like, and if not, proceeds to call `self.loc[key]`. 
2. However, when the key is a list, the function goes on to check if the key is also an instance of `Index`, leading to an incorrect branch where key_type is inferred as "integer".
3. This incorrect inference of key_type as "integer" causes the function to choose the wrong path for indexing, resulting in a KeyError when dealing with lists containing no matches.

### Bug Fix Strategy:
The bug can be fixed by adjusting the conditional statements for handling different types of keys. Specifically, ensure that the behaviour of list indexers aligns with that of other array-like indexers.

### Corrected Version of the _get_with Function:
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

    elif not is_list_like(key) or isinstance(key, (np.ndarray, Series, Index)):
        # Handle list, np.ndarray, Series, and Index indexers
        return self.loc[key]

    return self.reindex(key)
```

By making the necessary adjustments to the conditional statements, the corrected version ensures consistent behavior across different types of indexers, resolving the issue described in the GitHub post.