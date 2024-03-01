## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of key types and the logic surrounding determining how to index the Series based on the key type. The key type is inferred using the `infer_dtype` function, but the logic that follows does not account for all possible key types.

In Case 1, Case 2, and Case 3, the key type is inferred correctly as a string, but the subsequent logic does not handle this case properly. This leads to returning incorrect results and failing tests.

## Bug Fix Strategy
To fix the bug, we need to adjust the logic for handling different key types. Specifically, we need to ensure that when the key type is determined to be a string, the correct indexing method (loc or iloc) is applied to the Series.

## Corrected Code
```python
# this is the corrected version of the _get_with function
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

    # Handle the case when key_type is inferred as 'string'
    if key_type == "string":
        return self.loc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

The corrected code now correctly handles the case when the key type is inferred as a 'string' by using the `self.loc` method for indexing the Series.