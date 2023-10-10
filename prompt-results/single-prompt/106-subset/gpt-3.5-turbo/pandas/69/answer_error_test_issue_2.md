To fix the bug, you need to modify the `_convert_key` method in the `_AtIndexer` class. Specifically, you need to change the condition for raising the `ValueError` to check if the index is an integer index, instead of checking if it is a non-integer index. This will ensure that for an integer index, only integer indexers are allowed.

Here's the modified code snippet:

```python
@Appender(IndexingMixin.at.__doc__)
class _AtIndexer(_ScalarAccessIndexer):
    _takeable = False

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
                if isinstance(i, int) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on a non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```

By making this change, the program will pass the failed test without affecting other successful tests.