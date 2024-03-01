The issue in the `_get_with` function arises from the handling of the key parameter when it is not list-like. The function incorrectly assumes that if the key is not list-like, it should be accessed using `self.loc`. However, in some cases like when key is a single value, this approach fails.

To fix this bug, we need to modify the handling of non-list-like keys and ensure that key is appropriately indexed to avoid the KeyError. We can use the `self.loc` approach only when key is list-like, and otherwise directly return the key without trying to use it for indexing.

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

    if is_list_like(key):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)

        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:
            # handle duplicate indexing case
            return self.loc[key]
    else:
        return key
```

This corrected version ensures that key is returned directly when it is not list-like, preventing incorrect indexing attempts. This change should address the KeyError issues in the failing tests.