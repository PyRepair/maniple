#### Analysis:
- The `key` values provided in the failing test cases are different types of data structures like list, ndarray, Index, and Series.
- The function `_get_with` checks the type of the input `key` and performs different actions based on the type.
- The issue is related to how the function handles certain types of indexers, resulting in KeyError when indexing with a list.
- The key_type inferred in the function is causing the issue when key is a list.

#### Bug Cause:
- The bug arises because when the key is a list, the function incorrectly infers the key_type as `'string'` which later leads to an incorrect handling of the indexing operation.

#### Fix Strategy:
- Update the logic for inferring the key_type when the key is a list to ensure correct handling of the list indexer.
- Adjust the return statements to properly index with a list.

#### Corrected Function:
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

    elif not is_list_like(key):
        return self.loc[key]

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

        if isinstance(key, list):
            return self.loc[key]

    return self.reindex(key)
```

By making these changes, the function should now correctly handle indexing with a list and pass the failing test cases related to KeyErrors.