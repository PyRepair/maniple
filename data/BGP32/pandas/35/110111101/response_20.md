### Explanation
The error occurs when trying to access attributes of a `NoneType` object in the `_engine` function. This is likely due to the `_engine_type` method not correctly initializing the engine instance.

### Solution
Ensure that the `_engine_type` method initializes the engine instance properly before returning it.

### Corrected code
```python
@cache_readonly
def _engine(self):
    period = weakref.ref(self)
    engine = self._engine_type(period, len(self))
    if engine is None:
        engine = self._engine_type(period, len(self))
    return engine
```