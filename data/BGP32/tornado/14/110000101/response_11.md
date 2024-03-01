The buggy function `initialize` is intended to set the current `IOLoop` instance based on the `make_current` argument provided. The issue in the current implementation is that it incorrectly handles the case when `make_current` is `True` and there is already a current `IOLoop` instance.

### Bug Explanation:
- When `make_current` is `True`, the function should check if there is already a current `IOLoop` instance. If there is, it should raise a `RuntimeError`.
- However, the current implementation only checks if there is no current instance and then calls `self.make_current()` which is incorrect.

### Bug Fix Strategy:
- Modify the condition when `make_current` is `True` to first check if there is already a current instance of `IOLoop`. If there is, raise a `RuntimeError` immediately.
- Only call `self.make_current()` if there is no current instance and `make_current` is `True`.

### Corrected Version:
```python
def initialize(self, make_current=None):
    existing_instance = IOLoop.current(instance=False)

    if make_current:
        if existing_instance is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
    elif make_current is None and existing_instance is None:
        self.make_current()
``` 

This corrected version ensures that the `make_current` parameter is handled correctly, checking for the presence of a current `IOLoop` instance before trying to set a new one.