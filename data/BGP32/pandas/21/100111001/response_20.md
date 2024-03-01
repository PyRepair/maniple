### Bug Analysis:
The `_get_with` function is intended to handle various types of keys for indexing a Series. However, there is a bug specifically related to handling non-matching keys when trying to fetch values from the Series. This bug leads to a KeyError not being raised as expected in the failing test scenarios. 

In the failing test, the key used for indexing the Series does not exist in the Series index, resulting in an expected KeyError. However, due to the incorrect handling of key types within the `_get_with` function, the KeyError is not raised as expected.

The issue arises with how the `key` parameter is processed in the function, leading to incorrect type inferences and consequently not raising the expected KeyError.

### Bug Fix Strategy:
To fix this bug, the function `_get_with` needs to be modified to correctly handle the different types of keys and ensure that when a non-existent key is provided, a KeyError is raised.

### Corrected Version of the Function:
```python
def _get_with(self, key):
    if isinstance(key, slice):
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    
    if isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    
    if isinstance(key, tuple):
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

    if isinstance(key, list):
        return self.loc[key]

    if key_type == "string":  # assuming 'string' should represent the key type
        raise KeyError(f"None of {key} are in the {self.index}")
    
    return self.reindex(key)
```

By making the above changes, the function should now correctly handle different types of keys and raise a KeyError when the key is not found in the Series index.