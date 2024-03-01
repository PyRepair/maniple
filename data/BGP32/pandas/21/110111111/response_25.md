The bug in the `_get_with` function of the `Series` class is related to the way it handles different types of indexers, especially when using a list indexer. The function fails to handle list-like indexers correctly, leading to a KeyError in certain cases.

### Bug Description:
The function `_get_with` in the `Series` class has issues when dealing with list-like indexers. It incorrectly processes the key in some scenarios, leading to a KeyError when trying to access the series with that key. This inconsistency in handling different types of indexers causes the failing tests to occur.

### Bug Location:
The bug arises in the section of the code where it tries to handle various types of key inputs, specifically the list-like key handling.

### Cause of the Bug:
- The key is expected to be a list-like input, but the function fails to correctly process it, leading to a KeyError.
- The function checks the type of the key and tries to handle it differently based on the type, resulting in inconsistent behavior.

### Strategy for Fixing the Bug:
To fix this bug, we need to ensure that the function handles list-like indexers correctly. It should treat list, ndarray, Index, and Series indexers consistently, preventing the KeyError from occurring. By updating the implementation to address list-like key inputs uniformly, we can resolve this issue.

### Corrected Version of the `_get_with` Function:
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    if not is_list_like(key):
        key = [key]
    
    key = np.asarray(key)
    
    if key.dtype == object:
        key = key.astype(self.index.dtype)
    
    return self.reindex(key)
```

By making the above corrections, the `_get_with` function should now handle list-like indexers consistently, resolving the KeyError and passing the failing tests.

Ensure to incorporate this corrected version of the function into the `pandas/core/series.py` file.