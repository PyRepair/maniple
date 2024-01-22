# Complete corrected function code
```python
def _convert_key(self, key, is_setter: bool = False):
    """
    Require the keys to be the same type as the index. (so we don't
    fallback)
    """
    # allow arbitrary setting
    if is_setter:
        return list(key)

    for ax, i in zip(self.obj.index, key):
        if ax.is_integer() and not isinstance(i, (int, np.integer)):
            raise ValueError(
                "At based indexing on an integer index "
                "can only have integer indexers"
            )
        elif not ax.is_integer() and isinstance(i, (int, np.integer)):
            raise ValueError(
                "At based indexing on a non-integer "
                "index can only have non-integer "
                "indexers"
            )
    return key
```