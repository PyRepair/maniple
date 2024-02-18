## Bug Fix

The bug in the `initialize` function of the `IOLoop` class is that the condition for raising a `RuntimeError` is not properly handled. The function is designed to initialize the IOLoop instance by checking if it's current, and if not, it tries to make it current based on the `make_current` argument. If `make_current` is True and the IOLoop is already current, it should raise a `RuntimeError`. However, currently, it's not raising the error properly.

To fix this bug, the condition for raising the `RuntimeError` should be placed inside the `elif make_current` block, and the condition should check if an IOLoop already exists.

Here's the corrected code for the `initialize` function to fix the bug:

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

With this correction, the `initialize` function should now properly handle the condition for raising a `RuntimeError` when the current IOLoop instance already exists.

This fix resolves the issue reported on GitHub and ensures that the `initialize` function behaves as intended.