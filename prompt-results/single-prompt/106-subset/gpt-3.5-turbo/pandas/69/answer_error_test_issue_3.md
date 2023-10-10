To fix the bug, we need to modify the `_convert_key` method in the `_AtIndexer` class. Specifically, we need to check if the key is a float and if the corresponding axis is an integer index. If so, we should convert the key to an integer to match the index type.

Here's the fixed code snippet:

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

        # Convert key to integer if it's a float and the corresponding axis is an integer index
        converted_key = []
        for ax, i in zip(self.obj.axes, key):
            if isinstance(i, float) and ax.is_integer():
                i = int(i)
            converted_key.append(i)

        return tuple(converted_key)
```

With this fix, the program should pass the failed test without affecting other successful tests.