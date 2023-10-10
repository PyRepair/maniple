```python
@Appender(IndexingMixin.at.__doc__)
class _AtIndexer(_ScalarAccessIndexer):
    _takeable = False

    def _convert_key(self, key, is_setter: bool = False):
        """
        Require they keys to be the same type as the index. (so we don't
        fallback)
        """
        # allow arbitrary setting
        if is_setter:
            return list(key)

        for ax, i in zip(self.obj.axes, key):
            if ax.is_integer():
                if not isinstance(i, int):  # Fix: Use isinstance() instead of is_integer()
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if isinstance(i, int) and not ax.holds_integer():  # Fix: Use isinstance() instead of is_integer()
                    raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```
The bug in the code is that it is using the `is_integer()` method instead of the `isinstance()` function to check for integer type. I have replaced the `is_integer()` calls with `isinstance()` calls in the `if` conditions. This should fix the bug and prevent the `ValueError` from being raised.