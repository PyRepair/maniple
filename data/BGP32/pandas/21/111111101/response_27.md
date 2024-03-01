The bug in the `_get_with` function arises from the incorrect handling of the input key types, leading to a KeyError. The function is not properly checking for certain input types and does not handle them correctly, causing the failing tests.

From the provided information:
1. The function tries to determine the `key_type` based on the input `key` which is either a slice, DataFrame, tuple, scalar, or list-like object. In the failing test cases, the key is of type list, ndarray, Index, or Series.
2. The function incorrectly infers the `key_type` as "string" for all cases, which is not a valid type considered in the subsequent logic.
3. Based on the input `key_type`, the function decides whether to use positional or label-based indexing. However, the incorrect inference of `key_type` leads to incorrect indexing, resulting in KeyError.

To fix the bug, we need to correctly infer the `key_type` based on the input `key` and handle each type appropriately.

Here is the corrected version of the `_get_with` function:

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

    if not is_list_like(key):
        # Handle scalar values
        if key not in self.index:
            raise KeyError(f"{key} not found in the index")
        return self.loc[key]

    key = list(key)

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    key_type = lib.infer_dtype(key, skipna=False)

    if key_type == "integer":
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    # Handle the case when key is a list
    return self.loc[key]
```

With this correction, the function will correctly handle different types of keys including scalar, list, ndarray, Index, and Series, avoiding the KeyError issue. The corrected function should now pass the failing tests with the expected input/output values.