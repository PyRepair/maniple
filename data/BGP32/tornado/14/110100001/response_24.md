## Analysis
The `initialize` function in the `IOLoop` class is supposed to initialize the `IOLoop` instance and make it the current instance if `make_current` is specified. However, the current implementation is incorrect and causing the test `test_force_current` to fail.

## Bug Identification
- The bug occurs when `make_current` is `True` and there is already a current `IOLoop` instance. Instead of raising `RuntimeError` when another `IOLoop` instance is attempted to be made current, it allows the new instance to be made current.
- The bug is causing the test `test_force_current` to fail because it expects an exception to be raised when trying to make a second `IOLoop` instance current.

## Bug Cause
The bug occurs because the condition to raise `RuntimeError` when `IOLoop.current(instance=False)` is not None is misplaced. It should be checked before attempting to make the instance current.

## Bug Fix Strategy
To fix the bug, the logic of checking the current instance should be adjusted to handle the case when `make_current` is `True`. If there is already a current instance and `make_current` is `True`, it should raise an exception.

## Corrected Code
```python
class IOLoop(Configurable):
    ...

    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:  # Fixed the condition here
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

By adjusting the condition to check if a current `IOLoop` instance already exists when `make_current` is `True`, the bug should be fixed and the test `test_force_current` should pass successfully.