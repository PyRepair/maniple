### Analysis:
1. The buggy function `initialize` in the `IOLoop` class is checking if an `IOLoop` instance already exists without considering the case when `make_current=True`.
2. The test function `test_force_current` is attempting to create a new `IOLoop` instance with `make_current=True`, which should raise a `RuntimeError` if an `IOLoop` instance already exists.

### Bug Cause:
The bug is caused by the `initialize` function not handling the case when `make_current=True` correctly. It only checks for the existence of an `IOLoop` instance when `make_current` is `None` or `False`, leading to the incorrect `RuntimeError`.

### Fix Strategy:
To fix the bug, we need to ensure that when `make_current=True`, the `initialize` function should raise a `RuntimeError` if an `IOLoop` instance already exists.

### Corrected Version:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current: # Changed condition
        if IOLoop.current(instance=False) is not None: # Check if current IOLoop instance exists
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By changing the condition for `make_current=True` and checking if an `IOLoop` instance already exists in that case, the corrected version should now pass the failing test and resolve the issue reported on GitHub.