### Analysis:
1. The `initialize` method in the `IOLoop` class is supposed to handle the initialization process of an IOLoop object. 
2. The `make_current` parameter is used to determine if the current IOLoop instance should be set as the current one.
3. The bug occurs when the `make_current` parameter is set to `True` and there is already a current IOLoop instance.
4. The failing test `test_force_current` is trying to create an IOLoop instance by setting `make_current=True`, and then attempting to create another IOLoop instance with `make_current=True` which should raise a `RuntimeError`.

### Bug:
The bug in the existing code arises when `make_current=True`, but there is already an existing current IOLoop instance. In this scenario, the code incorrectly tries to create a new IOLoop instance and then raises a `RuntimeError` when it detects that a current IOLoop already exists.

### Strategy for fixing the bug:
1. Check if a current IOLoop instance already exists when `make_current=True`.
2. If a current IOLoop instance already exists, raise a `RuntimeError` immediately.
3. Avoid creating a new instance in this situation.

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