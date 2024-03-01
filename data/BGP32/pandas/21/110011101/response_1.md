### Bug Explanation
The bug is in the `_get_with` function of the `Series` class. The issue arises from the condition where the type of `key` is tested. If `key` is not a list-like object, the function attempts to access `self.loc[key]`. However, when `key` is a one-element Series, ndarray, or Index (not list-like), this lookup operation raises a KeyError because the value is not in the Series index. This situation is not handled correctly in the current implementation.

### Bug Fix Strategy
To fix the bug, we need to modify the condition for non-list-like `key` objects to handle these specific cases properly. Instead of directly trying to perform a lookup with `self.loc[key]`, we can check if `key` is an instance of Series, ndarray, or Index, and then convert it to a list before the lookup operation.

### Corrected Code
Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError("Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column")
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    # Handle non-list-like key types
    if isinstance(key, (np.ndarray, Series, Index)):
        key = key.tolist()
        
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

    return self.reindex(key)
```

This corrected version ensures that the function handles non-list-like `key` objects correctly and converts them to lists before performing lookups, which resolves the KeyError issues observed in the failing test cases.