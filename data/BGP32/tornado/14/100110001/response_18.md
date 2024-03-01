### Analysis:
1. The buggy function `initialize` in `tornado/ioloop.py` checks if a current `IOLoop` instance already exists before setting it as the current instance.
2. The failing test `test_force_current` in `tornado/test/ioloop_test.py` creates an `IOLoop` instance with `make_current=True`, then attempts to create another instance with the same flag set to `True` which should raise a `RuntimeError`.
3. The error message shows that the `RuntimeError: current IOLoop already exists` is raised when trying to create a new `IOLoop` instance with `make_current=True`.
4. The bug occurs because the implementation does not correctly handle the case when a current `IOLoop` instance already exists and a new one is being created with `make_current=True`.
5. To fix the bug, we need to check for the existence of a current `IOLoop` instance before raising an exception.

### Bug Fix:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

After fixing the above bug, the corrected function correctly checks if a current `IOLoop` instance already exists before attempting to set it as the current instance with `make_current=True`. This fix ensures that a `RuntimeError` is raised if a current `IOLoop` instance already exists when trying to create a new one with `make_current=True`.