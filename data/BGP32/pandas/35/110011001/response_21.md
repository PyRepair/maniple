### Analysis
The `AttributeError: 'NoneType' object has no attribute 'view'` error indicates that the `_engine` attribute is returning `None` instead of the expected `PeriodEngine` object. This leads to an AttributeError when trying to access the `view` attribute on a `NoneType` object.

### Bug
The `_engine` function is not correctly returning an instance of the `PeriodEngine` class, leading to the `NoneType` error.

### Fix
Ensure that the `_engine` function returns a valid instance of the `PeriodEngine` class.

### Corrected Version
```python
@cache_readonly
def _engine(self):
    # To avoid a reference cycle, pass a weakref of self to _engine_type.
    period = weakref.ref(self)
    return self._engine_type(period, len(self))()
``` 

By adding `()` at the end of `self._engine_type(period, len(self))`, the `PeriodEngine` instance is created and returned properly.