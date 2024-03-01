### Analysis:
- The `initialize` function in the `IOLoop` class is used to set up the IOLoop instance.
- The `initialize` function checks if a current IOLoop instance already exists before creating a new one with the `make_current` parameter.
- The failing test `test_force_current` is trying to create an IOLoop instance with `make_current=True`, which should fail if a current IOLoop instance already exists.

### Issue:
- The buggy function does not handle the case where a current IOLoop instance already exists correctly. It checks if `make_current` is `True` but does not verify if `IOLoop.current(instance=False)` is not `None`.

### Proposed Fix:
- Modify the condition in the `elif` block to check if `IOLoop.current(instance=False)` is not `None` before raising a `RuntimeError`.
- Ensure that the `make_current()` function is called only when needed.

### Corrected Version:
```python
def initialize(self, make_current=None):
    current_instance = IOLoop.current(instance=False)
    if make_current is None:
        if current_instance is None:
            self.make_current()
    elif make_current:
        if current_instance is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
``` 

After applying this correction, the `initialize` function should behave correctly, and the failing test should pass without raising any `RuntimeError`.