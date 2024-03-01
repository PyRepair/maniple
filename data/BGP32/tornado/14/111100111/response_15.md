### Analysis:
1. The `initialize` function in the `IOLoop` class checks if the `make_current` parameter is `None`, `True`, or `False`, and then proceeds accordingly.
2. The bug occurs when checking if an `IOLoop` instance already exists using `IOLoop.current(instance=False)`. If it returns `None`, it should not raise an error "current IOLoop already exists" when `make_current` is set to `True`.
3. The failing test `test_force_current` expects that when `make_current=True`, a new `IOLoop` instance is created, and subsequent creation attempts with `make_current=True` should raise a `RuntimeError`.
4. The bug is caused by the incorrect logic in the `initialize` function where the condition for raising a `RuntimeError` is flawed.

### Bug Fix Strategy:
1. Update the condition where the `RuntimeError` is raised. If `make_current` is `True` and `IOLoop.current(instance=False)` returns `None`, then do not raise a `RuntimeError` as there is no existing `IOLoop` instance.
2. Ensure that when `make_current` is passed as `True`, the new instance is made current by calling the `make_current` function.

### Corrected Version:
```python
def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:  # Check if an instance already exists
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

By updating the condition for raising a `RuntimeError` to check if an `IOLoop` instance exists when `make_current=True`, we can fix the bug.

After applying this correction, the `initialize` function should behave as expected and pass the failing test case.