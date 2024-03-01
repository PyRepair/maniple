### Bug Explanation
The bug occurs because the function `_get_with` fails to handle cases where the key parameter is a non-list-like datatype or a scalar value correctly. This leads to the function trying to access the key as a list, numpy array, ExtensionArray, Series, or Index when it doesn't fall into any of these categories, ultimately causing a KeyError to not be raised as expected in the test cases.

### Bug Fix Strategy
To fix the bug, we need to modify the `_get_with` function to properly handle non-list-like datatypes or scalar values. We can check if the key is a scalar value and handle it appropriately.

### The corrected function
```python
def _get_with(self, key):
    # other: fancy integer or otherwise
    if isinstance(key, slice):
        # _convert_slice_indexer to determine if this slice is positional
        # or label-based, and if the latter, convert to positional
        slobj = self.index._convert_slice_indexer(key, kind="getitem")
        return self._slice(slobj)
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not "
            "supported, use the appropriate DataFrame column"
        )
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)

    # Check for scalar values
    if is_scalar(key):
        return self.loc[key]

    # Handle other cases
    if not is_list_like(key):
        # e.g. scalars that aren't recognized by lib.is_scalar, GH#32684
        return self.loc[key]

    if not isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        key = list(key)

    if isinstance(key, Index):
        key_type = key.inferred_type
    else:
        key_type = lib.infer_dtype(key, skipna=False)

    # Note: The key_type == "boolean" case should be caught by the
    # com.is_bool_indexer check in __getitem__
    if key_type == "integer":
        # We need to decide whether to treat this as a positional indexer
        # (i.e. self.iloc) or label-based (i.e. self.loc)
        if not self.index._should_fallback_to_positional():
            return self.loc[key]
        else:
            return self.iloc[key]

    if isinstance(key, list):
        # handle the dup indexing case GH#4246
        return self.loc[key]

    return self.reindex(key)
```

By introducing a check for scalar values and returning the corresponding value using `loc`, we ensure that the function handles all types of keys correctly and raises a KeyError when needed.