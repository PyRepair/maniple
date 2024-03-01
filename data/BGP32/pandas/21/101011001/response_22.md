### Bug Analysis
The bug in the `_get_with` function is caused by incorrectly handling the case when `key` is a list or array of values not present in the Series index. The function incorrectly tries to retrieve the values from the Series using `loc` which leads to a KeyError when the values are not found in the index.

### Bug Explanation
1. In the failing tests, for all cases, the `key` values are not present in the Series index.
2. The function tries to infer the `key_type`, which is identified as `'string'` in all cases.
3. Based on the `key_type` being `'string'`, the function incorrectly tries to use `self.loc[key]`, which results in a KeyError.

### Bug Fix Strategy
To fix the bug, we need to modify the logic for handling cases when `key` is a list or array of values not present in the Series index. Instead of trying to access the values directly using `loc`, we should check for the presence of the values in the index before attempting to retrieve them.

### Corrected Function
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

    elif not is_list_like(key):
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
        key_set = set(key)
        missing_values = key_set.difference(self.index)
        if missing_values:
            raise KeyError(f"None of {list(key_set)} are in the index")
        return self.loc[key]

    return self.reindex(key)
```

With this corrected version, the function should now properly handle cases where the `key` values are not present in the Series index and avoid raising a KeyError.