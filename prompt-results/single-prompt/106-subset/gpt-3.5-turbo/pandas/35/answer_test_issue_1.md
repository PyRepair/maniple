```python
import weakref

def cache_readonly(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

class FixedClass:
    @cache_readonly
    def _engine(self):
        # To avoid a reference cycle, pass a weakref of self to _engine_type.
        period = weakref.ref(self)
        return self._engine_type(period() if period else None, len(self))

def test_get_level_values_when_periods():
    from pandas import Period, PeriodIndex, MultiIndex

    idx = MultiIndex.from_arrays(
        [PeriodIndex([Period("2019Q1"), Period("2019Q2")], name="b")]
    )
    idx2 = MultiIndex.from_arrays(
        [idx._get_level_values(level) for level in range(idx.nlevels)]
    )
    assert all(x.is_monotonic for x in idx2.levels)

test_get_level_values_when_periods()
```