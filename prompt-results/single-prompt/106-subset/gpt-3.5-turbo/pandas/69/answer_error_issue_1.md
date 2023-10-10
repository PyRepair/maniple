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

        key = list(key)  # Convert key to a list

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
        return key
```

In the given code snippet, the issue is with the error message string in the `raise ValueError` statement. It states "At based indexing on an non-integer index can only have non-integer indexers", which is incorrect. The correct message should be "At based indexing on a non-integer index can only have non-integer indexers".

To fix the bug, you need to modify the `raise ValueError` statement to use the correct error message. Additionally, you need to convert the `key` to a list before the loop to ensure that it is iterable.

Once you make these changes, the program should pass the failed test without affecting other tests.