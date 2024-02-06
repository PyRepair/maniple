The issue with the _get_with function lies within the conditional blocks that handle different types of input `key`. When the input `key` is of type list, it is not appropriately handled, leading to unexpected behavior and inaccuracies in the error messages. 

The `key` is not being properly processed within the conditional checks, causing the function to fall through to the final conditional block, where it returns the result of `self.reindex(key)`.

To address this issue, the conditional logic in the function needs to be revised to accurately classify and handle different types of input `key`, ensuring that each conditional block returns the expected result based on the input type. Additionally, the implementation of `self.reindex` may need to be reviewed and potentially revised to ensure it correctly handles the input `key`.

Here's the corrected version of the _get_with function with the revised conditional logic and handling for different types of input `key`:

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
    elif is_list_like(key) and not isinstance(key, (np.ndarray, Series, Index)):
        return self.loc[key]
    elif isinstance(key, (list, np.ndarray, Index)):
        key_type = lib.infer_dtype(key, skipna=False)
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        else:  # Handle non-integer type key
            return self.loc[key]
    else:  # Handle other cases
        return self.reindex(key)
```

This revised version of the function includes a re-evaluation of the conditional logic to accurately classify and handle different types of input `key`, ensuring that each conditional block returns the expected result based on the input type. The improvements made to the conditional blocks address the handling of list-like and non-list-like input `key`, as well as different input types such as ndarray and Index.

By implementing these changes, the function should now correctly handle different types of input `key` and provide the expected results for each case, resolving the issues identified in the test case.