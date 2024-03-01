### Error Analysis:
- The buggy function `initialize` in `tornado/ioloop.py` is supposed to handle the initialization of the IOLoop instance with the option to make it the current instance.
- The failing test `test_force_current` in `tornado/test/ioloop_test.py` is trying to create two instances with `make_current=True` and expects the second one to raise a `RuntimeError`.
- The error message indicates that the `initialize` function is incorrectly throwing a `RuntimeError` when `make_current` is set to `True` and there is already an existing current IOLoop instance.
- The GitHub issue points out the confusion in the logic at line 252 of `ioloop.py` where the code checks if the current instance is `None` and then raises an error for "already exists".

### Bug Cause:
- The bug occurs because when `make_current` is `True`, the code should only raise an error if there is already a current IOLoop instance, but the current implementation raises an error even if no current instance exists.

### Bug Fix Strategy:
1. Modify the `initialize` function to only raise a `RuntimeError` when `make_current` is `True` and there is already an existing IOLoop instance.
2. Ensure that the logic correctly handles the scenario when `make_current` is `None` and sets the current instance if it doesn't exist.

### Corrected Version:
```python
def initialize(self, make_current=None):
    current_instance = IOLoop.current(instance=False)
    if make_current is None:
        if current_instance is None:
            self.make_current()
    elif make_current:
        if current_instance:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

With the corrected version, the `initialize` function should now behave correctly and pass the failing test `test_force_current` without raising an unnecessary `RuntimeError`.