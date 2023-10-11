To fix the bug, we need to ensure that integer values are not allowed for non-integer indexes when using the `at` method. 

To do this, we can modify the `_convert_key` method to raise a `ValueError` when an integer value is provided for a non-integer index. Here's the fixed code:

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
            if not isinstance(i, int):
                raise ValueError(
                    "At based indexing on an integer index "
                    "can only have integer indexers"
                )
        else:
            if isinstance(i, int):
                raise ValueError(
                    "At based indexing on a non-integer "
                    "index can only have non-integer "
                    "indexers"
                )
    return key
```