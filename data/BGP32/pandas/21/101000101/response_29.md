The bug in the `_get_with` function arises from the incorrect handling of different types of `key` inputs. The function fails to properly identify the type of the `key` variable, leading to errors. 

To fix this issue, we need to revise the logic for determining the type of `key` and its subsequent processing based on that type. By properly identifying the type of `key`, we can handle each case correctly and ensure the function returns the expected results.

Here is the corrected version of the `_get_with` function:

```python
def _get_with(self, key):
    if isinstance(key, (list, np.ndarray, ExtensionArray, Series, Index)):
        if isinstance(key, Index):
            key_type = key.inferred_type
        else:
            key_type = lib.infer_dtype(key, skipna=False)
        
        if key_type == "integer":
            if not self.index._should_fallback_to_positional():
                return self.loc[key]
            else:
                return self.iloc[key]
        
        # handle the dup indexing case GH#4246
        return self.loc[key]
    
    elif is_scalar(key):
        return self.loc[key]
    
    elif isinstance(key, ABCDataFrame):
        raise TypeError(
            "Indexing a Series with DataFrame is not supported, use the appropriate DataFrame column"
        )
    
    elif isinstance(key, tuple):
        return self._get_values_tuple(key)
    
    else:
        raise ValueError("Unsupported key type")
```

This corrected version ensures that the key type is properly identified and processed accordingly, based on the expected behavior outlined in the provided test cases.