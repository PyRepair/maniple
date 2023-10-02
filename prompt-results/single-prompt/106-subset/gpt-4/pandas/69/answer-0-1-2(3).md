The error is caused due to the function "is_integer(i)" which checks whether the index is an integer or not. However, in the current context, an input like 4.0 (which is actually an integer) is being considered as a non-integer because the function "is_integer(i)" checks the specific type, not just the value. 

To fix these errors, we need to alter the function "is_integer()" to return True when a float value is actually an integer. 

Here's the fixed code

Add this function to somewhere in the program:

```python
def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False
```

And alter the function _convert_key:

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
                if not is_integer_num(i):
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if is_integer_num(i) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```

Note that we are replacing the function 'is_integer(i)' with 'is_integer_num(i)' which can appropriately check if a float value is actually an integer or not. This change should solve the problem and let the test case pass properly.