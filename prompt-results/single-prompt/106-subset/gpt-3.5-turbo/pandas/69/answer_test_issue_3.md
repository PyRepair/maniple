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
                if not pd.core.dtypes.common.is_integer(i):  # Fix: Use fully qualified function name
                    raise ValueError(
                        "At based indexing on an integer index "
                        "can only have integer indexers"
                    )
            else:
                if pd.core.dtypes.common.is_integer(i) and not ax.holds_integer():  # Fix: Use fully qualified function name
                    raise ValueError(
                        "At based indexing on a non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```