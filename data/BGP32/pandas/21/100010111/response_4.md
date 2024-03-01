### Analysis
1. The buggy function `_get_with` is meant to handle different types of indexers for the Series object. It checks the type of the `key` parameter and then performs specific actions based on the type.
2. The failing test cases expect specific behavior when using different types of indexers (`list`, `array`, `Index`, `Series`).
3. The error messages indicate that the KeyError is being raised when using certain types of indexers, which is inconsistent with the expected behavior.
4. The expected behavior is that when a key does not match any index values, a KeyError should be raised consistently across different types of indexers.
5. The issue on GitHub points out the inconsistency in behavior when using different types of indexers and suggests aligning the behavior to make it consistent.

### Bug Cause
The bug in the `_get_with` function is caused by inconsistent handling of different types of indexers. When a key does not match any index values, a KeyError should be raised regardless of the type of indexer. However, the current implementation raises KeyError for some types of indexers but not for others, leading to inconsistent behavior.

### Bug Fix Strategy
To fix the bug:
1. Ensure that for all types of indexers (`list`, `array`, `Index`, `Series`), if the key does not match any index values, a KeyError is consistently raised.
2. Simplify the logic for handling different types of indexers to achieve consistent behavior.

### Corrected Function
```python
def _get_with(self, key):
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

    if not is_list_like(key):
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    # Check for key membership in the index and raise a KeyError if not found
    if any(k not in self.index for k in key):
        raise KeyError(f"None of {key} are in the index")

    return self.reindex(key)
```

By including the check for key membership in the index and raising a KeyError if any key is not found in the index, the corrected function ensures consistent behavior across different types of indexers.