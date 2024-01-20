# The corrected function code
```python
    def _convert_key(self, key, is_setter: bool = False):
        """
        Require they keys to be the same type as the index. (so we don't
        fallback)
        """
        # allow arbitrary setting
        if is_setter:
            return list(key)
    
        for ax, i in zip(self.obj.axes, key):
            if isinstance(ax, pd.DatetimeIndex) or isinstance(ax, pd.TimedeltaIndex):
                if not isinstance(i, (pd.Timestamp, pd.Timedelta)):
                    raise ValueError(
                        "At based indexing on a datetime or timedelta index "
                        "can only have datetime or timedelta indexers"
                    )
            elif isinstance(ax, pd.Float64Index) or isinstance(ax, pd.Int64Index):
                if not isinstance(i, (float, int)):
                    raise ValueError(
                        "At based indexing on a float or integer index "
                        "can only have float or integer indexers"
                    )
            else:
                if type(ax) != type(i):
                    raise ValueError(
                        "At based indexing on an index of type {} "
                        "can only have indexers of the same type".format(type(ax).__name__)
                    )
        return key
```