The issue is that the `at` method is being called with an integer argument instead of a float argument. This is causing a `ValueError` to be raised. 

To fix this issue, we can modify the `at` method to cast the key to a float if it is an integer. This will match the behavior of the `loc` method. Here's the modified code snippet:

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
                key = float(i)  # cast key to float if it is an integer
            else:
                if is_integer(i) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```

With this modification, the program should pass the failed test without affecting other successful tests. Additionally, this fix can be easily applied to the original project.