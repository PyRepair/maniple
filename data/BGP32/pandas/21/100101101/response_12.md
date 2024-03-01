### Bug Analysis:
The bug in the `_get_with` function occurs when the input key is a list, np.ndarray, Index, or Series that does not exist in the Series index. The function incorrectly determines the `key_type` as `'string'`, leading to the wrong branch of code execution.

### Bug Explanation:
In all failing test cases, the key being passed to the function does not exist in the Series index. The function wrongly infers the `key_type` as `'string'` in these cases, which causes the function to not raise a `KeyError`, leading to incorrect behavior.

### Bug Fix Strategy:
To fix the bug, we need to properly handle the case where the `key` is not found in the Series index and correctly infer the `key_type`. We can check if the key is present in the index before inferring the type to ensure that the `KeyError` is raised when necessary.

### Corrected Function:
```python
def _get_with(self, key):
    if self.index.isin(key).all():
        return self.loc[key]
      
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
        return self.loc[key]

    return self.reindex(key)
``` 

The corrected function first checks if the `key` is present in the index using `isin(key).all()`. If the key is not present, it directly returns `self.loc[key]`, raising the `KeyError` as expected.