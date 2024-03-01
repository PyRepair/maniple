## Analysis
1. The buggy function `initialize` is supposed to initialize an IOLoop instance with a flag `make_current` to determine if it should be made the current instance.
2. The buggy function has an issue where it raises a `RuntimeError` if `make_current` is `True` and there is already a current IOLoop instance existing.
3. The failing test `test_force_current` tries to create an IOLoop instance with `make_current=True`, which should raise a `RuntimeError` due to the existing current IOLoop instance.
4. The error message indicates that the `RuntimeError` is triggered due to an existing current IOLoop instance when `make_current=True`.

## Bug Explanation
The bug occurs in the `initialize` function when it checks for the presence of a current IOLoop instance. If `make_current` is `True` and there is already a current instance, the function incorrectly raises a `RuntimeError`. Instead, it should only raise the error if `make_current` is `True` and there is no current instance.

## Bug Fix
To fix the bug, we need to update the logic in the `initialize` function. The `RuntimeError` should only be raised if `make_current` is `True` and there is already a current IOLoop instance. Here's the corrected version of the function:

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

By fixing the condition to raise `RuntimeError`, the function will now correctly handle the case when `make_current=True` and there is an existing current IOLoop instance.