### Bug Analysis:
The bug occurs when the input `key` is either a list, numpy array, Series, or Index, and the `key_type` is incorrectly inferred as `'string'` regardless of the actual type of `key`. This inaccurate inference of `key_type` leads to the wrong path being taken in the subsequent logic of the function, causing the KeyError to be raised when accessing `ser[key]`.

### Bug Explanation:
1. In all the provided failing test cases, the `key_type` is set to `'string'`, which suggests that the function is incorrectly inferring the type of input `key`.
2. This incorrect inference of `'string'` leads to the function returning `self.loc[key]` instead of taking the correct path.
3. Due to this erroneous behavior, when trying to access `ser[key]`, a KeyError is thrown because the type is not correctly handled.

### Bug Fix Strategy:
To fix this bug, we need to ensure that the type of `key` is correctly inferred and handled within the `_get_with` function. This involves correctly identifying the type of `key` such as list, numpy array, Series, or Index, and then applying the appropriate logic to access the data from `self`.

### Corrected Function:
Here is the corrected version of the `_get_with` function that addresses the bug:

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

    if is_list_like(key) and not isinstance(key, (Index, Series)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    if key_type in ['integer', 'floating']:
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    return self.reindex(key)
```

This corrected version includes the proper handling of different types of `key`, ensuring that the appropriate path is taken based on the inferred type.