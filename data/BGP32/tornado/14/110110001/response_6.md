### Analysis:
1. Buggy Function: `initialize(self, make_current=None)`
2. Buggy Class: `IOLoop`
3. Failing Test: `test_force_current`
4. Corresponding Error Message: `RuntimeError: current IOLoop already exists`

### Identified Error:
The error occurs in the `initialize` method of the `IOLoop` class when `make_current=True` and there is already a current `IOLoop` instance present. The buggy function incorrectly raises a `RuntimeError` in this scenario.

### Cause of the Bug:
The cause of the bug is that the `initialize` method does not correctly handle the case when `make_current=True` and a current `IOLoop` instance already exists. It should only try to make the current instance if there is no current instance present.

### Strategy for Fixing the Bug:
1. Check if `make_current` is `True` and there is already a current instance of `IOLoop` before attempting to make the instance current.
2. Only raise a `RuntimeError` if `make_current=True` and there is already a current instance.

### Corrected Function:
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

By implementing the corrected `initialize` method above, the issue should be resolved, and the failing test should pass without raising a `RuntimeError`.