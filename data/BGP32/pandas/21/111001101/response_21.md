### Bug Explanation:
The bug in the `_get_with` function arises from the handling of various types of `key` input. The function incorrectly assumes that a `key` of type `list`, `np.ndarray`, or `Index` should result in the same behavior, leading to erroneous outcomes. Additionally, the calculation of `key_type` is faulty, leading to incorrect branching based on the inferred data type of `key`.

### Bug Fix Strategy:
1. Correct the type checking to treat different types of `key` appropriately.
2. Fix the calculation of `key_type` to accurately determine the data type of `key`.
3. Provide distinct cases for handling different types of `key` to ensure proper indexing behavior.

### Corrected Version of the `_get_with` function:
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

    if not is_list_like(key):
        return self.loc[key]

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:
            return self.loc[key]

    return self.reindex(key)
``` 

This corrected version accounts for the various types of `key` inputs and ensures that the correct indexing operation is performed based on the inferred data type of `key`.