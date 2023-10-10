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
                if not is_integer(i):
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if is_integer(i) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on a non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
                elif not is_integer(i) and ax.holds_integer():
                    raise ValueError(
                        "At based indexing on an integer "
                        "index can only have integer "
                        "indexers"
                    )
        return key
```

To fix the bug, you need to modify the `_convert_key()` method as follows:
- Add an `elif` statement to check if the index holds integers and the indexer is not an integer. In this case, raise a `ValueError` indicating that "At based indexing on an integer index can only have integer indexers".
- Modify the `ValueError` message for the case when the index is not an integer to "At based indexing on a non-integer index can only have non-integer indexers".
- Add an `elif` statement to check if the index holds integers and the indexer is an integer. In this case, raise a `ValueError` indicating that "At based indexing on a non-integer index can only have non-integer indexers".

By making these changes, the program will pass the failed test without affecting the other successful tests.