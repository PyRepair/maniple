### Analysis
1. The `initialize` function of the `IOLoop` class initializes the IOLoop object.
2. When `make_current` is `True`, it should set the IOLoop object as the current IOLoop instance, but only if there is no current instance already present. If a current instance already exists, it should raise a `RuntimeError`.
3. The failing test `test_force_current` first creates an IOLoop object with `make_current=True`, then tries to create another one with the same parameter to test the `make_current=False` behavior.

### Bug
The bug in the `initialize` function is that it checks for the current instance before setting itself as the current instance, but it doesn't properly handle the case when there is already a current instance and `make_current=True`.

### Fix
To fix the bug, we should check if `make_current` is `True` and there is already a current instance before attempting to set the current instance. If these conditions are met, we should raise a `RuntimeError`.

### Corrected code
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