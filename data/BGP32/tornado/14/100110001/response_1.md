## Analysis
1. The buggy function `initialize` in the `IOLoop` class is responsible for handling the initialization of an IOLoop instance with an optional `make_current` flag.
2. The failing test `test_force_current` tries to create an IOLoop instance with `make_current=True` and expects that a RuntimeError should be raised if an IOLoop instance already exists.
3. The error message indicates that the RuntimeError is being raised when attempting to create a second IOLoop instance with `make_current=True`, but the test expects this behavior.
4. The bug occurs because the code does not properly handle the scenario where an IOLoop instance already exists when `make_current=True`. It should raise an error in this case as per the test expectations.
5. To fix the bug, we need to ensure that when `make_current=True` is passed, it checks if an IOLoop instance already exists and raises a RuntimeError if it does.

## Bug Fix
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

With this change, the `initialize` function will raise a RuntimeError when `make_current=True` and an IOLoop instance already exists, matching the behavior expected by the failing test case.