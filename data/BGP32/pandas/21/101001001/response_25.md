## Bug Explanation
The bug in the `_get_with` function arises from the incorrect handling of key types. The function checks if the key is not list-like, and if so, it tries to locate the key using `self.loc[key]`. However, there is an issue with the determination of `key_type` which results in treating the key as a string when it should not be.

In all the provided cases, the `key_type` is identified as `'string'` even when the key is a list or an array of objects. This incorrect classification causes the function to incorrectly proceed with treating the key as a string, leading to unexpected behavior and potential errors.

## Fix Strategy
To fix the bug, we need to adjust how the `key_type` is determined within the `_get_with` function. We should ensure that the correct type of the key is identified to facilitate the appropriate handling based on the key's actual structure.

One strategy could be to check the type of the key in a more granular way, distinguishing between various possible types such as lists, arrays, and scalars, and adjusting the logic accordingly. This revised approach should help in resolving the bug and ensuring the correct behavior of the function.

## Corrected Version of the Function

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

    if is_scalar(key):
        return self.loc[key]
    
    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        if isinstance(key, (np.ndarray, list)):
            key_type = lib.infer_dtype(key, skipna=False)
    
    # Note: The key_type == "boolean" case should be caught by the
    #  com.is_bool_indexer check in __getitem__
    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        return self.loc[key]

    return self.reindex(key)
```

In this corrected version of the function, we have adjusted the logic for determining the `key_type` to handle different types of keys appropriately. By checking if the key is a scalar first, we ensure that scalar keys are treated correctly. Then, for lists and arrays, we infer the dtype using `lib.infer_dtype` to accurately categorize the key type. Finally, we proceed with the necessary actions based on the corrected key type classification.