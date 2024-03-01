The bug in the `_get_with` function arises from the logic for handling different types of `key` inputs. 

In the provided function, the `key_type` is inferred based on the `key` input, but there is a discrepancy in how the `key` is processed. Specifically, when `key` is not recognized as list-like, the function attempts to access `self.loc[key]`, assuming it is a valid key for indexing. However, this can lead to an error if `key` is not valid for the `loc` indexer. 

To fix this bug, we can modify the logic for processing different types of `key` inputs. We can check for the type of `key` and handle each case accordingly, ensuring that the indexing operation (`self.loc`, `self.iloc`, or `self.reindex`) is performed correctly based on the type of `key`.

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

    # Check if key is scalar
    if not is_list_like(key) and not isinstance(key, (np.ndarray, ExtensionArray)):
        key = [key]

    # Determine the type of key
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
        # Explicitly check for list or ndarray
        if isinstance(key, (list, np.ndarray, ExtensionArray)):
            return self.loc[key]
        else:
            return self.reindex(key)
```

By explicitly handling scalar keys and different key types, the corrected function avoids errors related to invalid keys for indexing operations. This should fulfill the expected input/output values for the provided test cases.