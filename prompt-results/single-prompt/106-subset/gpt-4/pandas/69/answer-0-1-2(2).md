The test which is failing is expecting the `.at` indexer to be able to handle integer values for indexes which are actually floats. This is inconsistent with the pandas documentation (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html) which states that the indexers must be of the same type as the index. 

However, it seems that pandas did make this change to allow integer indexers and you would want to handle this case. The check for this is currently done in the `_convert_key` method of `_AtIndexer` which raises an error if the index is a non-integer and the indexer is an integer.

Let's modify the `_AtIndexer` class's `_convert_key` method so that it attempts to convert an integer indexer to float before checking if it should raise an error. Note that we attempt the conversion using `try`-`except` as it might fail if the index is multi-dimensional. 

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
                try:
                    # attempt to convert integer indexer to float
                    i_maybe_float = float(i) if is_integer(i) else i
                except TypeError:
                    # fail on multi-dimensional index
                    i_maybe_float = i
                
                if is_integer(i_maybe_float) and not ax.holds_integer():
                    raise ValueError(
                        "At based indexing on an non-integer "
                        "index can only have non-integer "
                        "indexers"
                    )
        return key
```
This modified piece of code changes an integer indexer to a float one (only if it's possible). This places `_AtIndexer._convert_key` in line with the required behavior. Might be worth revising the function documentation as well.