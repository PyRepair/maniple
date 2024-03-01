### Analysis:
The `_get_with` function in the `Series` class is designed to handle different types of keys for indexing a `Series` object. The function contains conditional blocks for different key types, such as slices, DataFrames, tuples, and non-list-like keys.

However, the bug seems to be related to the handling of keys that are lists, ndarrays, Index objects, or Series objects. In the provided failing tests, the function fails to raise a `KeyError` as expected when indexing with keys that do not exist in the index.

### Bug Explanation:
1. In the first conditional block, when `key` is not recognized as a slice, DataFrame, or tuple, and also not list-like, the function tries to index using `self.loc[key]`. If the `key` does not exist in the index, instead of raising a `KeyError`, it tries to use `self.loc[key]`, causing unexpected behavior.
   
2. The subsequent conditional blocks intended to handle keys that are not recognized as list-like or specific types like Index, np.ndarrays, etc., may result in incorrect behavior since they are not checking for the existence of the key in the index before proceeding further.

### Suggested Fix:
To fix the bug, we need to ensure that if the key does not exist in the index, the function raises a `KeyError` as expected. Additionally, we need to handle different key types appropriately to prevent unexpected behavior.

### Corrected Code:
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
        raise KeyError(f"KeyError: {key}")

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

By making these adjustments, the corrected function should now properly handle different types of keys and raise a `KeyError` when the key is not found in the index, passing the failing tests.