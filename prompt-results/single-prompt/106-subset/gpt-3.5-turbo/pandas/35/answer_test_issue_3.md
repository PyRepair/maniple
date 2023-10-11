To fix the bug, you can modify the `_engine` method to pass the weakref of `self` to `_engine_type` instead of `period`.

Here's the fixed code:

```python
from weakref import ref

def cache_readonly(func):
    def wrapper(self):
        attr_name = f"_{func.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper

@cache_readonly
def _engine(self):
    engine_type = ref(self._engine_type)
    return engine_type()(ref(self), len(self))
```

With this fix, the code should now pass the failing test case without affecting other successful tests.