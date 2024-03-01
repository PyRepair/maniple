### Bug Description
The bug occurs in the `_get_with` function when the key parameter is passed as a list, numpy array, Index, or Series. The function incorrectly assigns `key_type` based on the data type of the key, leading to an incorrect type inference in some cases. This causes the function to incorrectly choose the path for indexing the Series (`self.loc[key]` vs `self.iloc[key]`).

### Bug Fix Strategy
To fix the bug, we need to ensure that `key_type` is correctly determined based on the type of the key parameter. This will allow the function to choose the correct indexing method (`self.loc[key]` or `self.iloc[key]`) based on the inferred type of the key.

### Updated Buggy Function
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

    if is_scalar(key) or (is_list_like(key) and len(key) == 1):
        key = key[0]

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.loc[key]
```

### Update Explanation
- I added a condition to check if the key is a scalar or a list-like object with only one element. In such cases, we extract the single element to ensure `infer_dtype` receives the correct input.
- I modified the key_type determination based on the type of the key after any potential extraction.
- The function now correctly infers the key type and chooses the appropriate indexing method (`self.loc[key]` or `self.iloc[key]`) based on the key type inference.

By making these changes, the `_get_with` function should now correctly handle the indexing scenarios that were failing previously.