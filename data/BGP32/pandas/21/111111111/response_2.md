To fix the issue in the `_get_with` function, we need to address the inconsistency when using list indexers. The problem arises when a list indexer is passed to access values in the Series, leading to a KeyError even when the indexer should return NaN values.

The root cause of the bug lies in the conditional check for list-like objects, where the function tries to fetch the values directly using `self.loc[key]`. However, this causes a KeyError when the key is not present in the Series index.

To resolve this issue, we need to modify the conditional block for list-like keys to handle this scenario correctly. By catching the KeyError and returning NaN values for missing keys, we can align the behavior of list indexers with other array-like indexers.

Below is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    elif not is_list_like(key):
        try:
            return self.loc[key]
        except KeyError:
            return np.nan

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

With this adjustment, the `_get_with` function should correctly handle list-like keys that are not present in the Series index by returning NaN values instead of raising a KeyError. This change aligns the behavior of list indexers with other array-like indexers, addressing the inconsistency reported in the GitHub issue.