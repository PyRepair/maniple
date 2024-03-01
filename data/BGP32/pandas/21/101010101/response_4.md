### Analysis:
The buggy function `_get_with` is designed to handle different types of keys while accessing elements from a Series. However, the bug occurs when the key type is an ndarray or an Index. The bug leads to an incorrect inference of the key type, causing a mismatch with the actual key type.

The bug happens because the key type inference logic does not handle ndarray and Index types correctly, leading to the wrong branch being taken for key type comparison.

### Bug Fix Strategy:
To fix the bug, we need to adjust the logic for inferring the key type when the key is an ndarray or an Index type. We need to handle these cases separately to ensure the key type is correctly identified before processing the key.

### Corrected Version:

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

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    elif isinstance(key, np.ndarray):
        key_type = 'integer' if key.dtype.kind in 'iu' else 'string'
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

By improving the key type inference logic for ndarray and Index types, we ensure that the key type is correctly identified, resolving the bug and enabling the function to handle these cases correctly.