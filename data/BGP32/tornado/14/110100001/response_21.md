### Bug Analysis:
1. The `initialize` function in the `IOLoop` class is intended to set the current `IOLoop` instance if `make_current` is set to `True`.
2. The bug lies in the conditional statement for `make_current=True` where it checks if the current `IOLoop` instance is `None`. This leads to the function incorrectly handling the case where `make_current=True` and there is already a current `IOLoop` instance.
3. The failing test `test_force_current` expects that when a new `IOLoop` instance is created with `make_current=True`, it should raise a `RuntimeError` if there is already a current `IOLoop` instance, but the buggy function is not raising the error correctly.

### Bug Fix Strategy:
1. Update the `initialize` function in the `IOLoop` class to correctly handle the case where `make_current=True` and there is already a current `IOLoop` instance.
2. If `make_current=True` and a current instance exists, raise a `RuntimeError` indicating that the current `IOLoop` already exists.

### Corrected Version:
```python
# The corrected version of the initialize function
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

After implementing this corrected version of the `initialize` function, it should pass the failing test `test_force_current`.