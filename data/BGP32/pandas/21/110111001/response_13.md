The bug in the `_get_with` function lies in the logic to handle different types of keys when indexing a Series. The function is not correctly identifying the type of key when it is a non-list-like object, leading to incorrect behavior.

To fix the bug, we need to adjust the logic for handling non-list-like keys in order to properly index the Series based on the key type.

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
    elif isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:
            return self.reindex(key)
    else:
        # This handles the case of non-list-like keys
        return self.loc[key]

```

With this correction, the function now properly handles non-list-like keys by using `self.loc[key]` for such cases, ensuring that the correct indexing operation is performed regardless of the type of key.

This correction should address the bug and make the function work as expected, passing the failing tests provided.