```python
def _convert_key(self, key, is_setter: bool = False):
    """
    Require the keys to be the same type as the index. (so we don't
    fallback)
    """
    # allow arbitrary setting
    if is_setter:
        return list(key)
    
    for ax, i in zip(self.obj.axes, key):
        if ax.is_integer():
            if not is_integer(i):
                raise ValueError(
                    "At based indexing on an integer index "
                    "can only have integer indexers"
                )
        else:
            if ax.dtype.kind == 'i' and not ax.holds_integer():
                raise ValueError(
                    "At based indexing on a non-integer "
                    "index can only have non-integer "
                    "indexers"
                )
    return key
```

Explanation:
- In the original code, the condition `is_integer(i)` is used to check if the index is an integer, but this condition is incorrect.
- To fix the bug, we need to change the condition to check the dtype of the index instead.
- The modified code uses `ax.dtype.kind` to check if the index is an integer and then raises a `ValueError` accordingly.