### Analysis:
- The `initialize()` function in the `IOLoop` class is responsible for setting the current `IOLoop` instance.
- The bug occurs when trying to make the current `IOLoop` instance if `make_current=True` and there is already a current instance.
- The bug is related to incorrect logic in checking for the existence of a current `IOLoop` instance and handling the case when `make_current=True`.
- The failing test `test_force_current` specifically tests the behavior when trying to create a new current `IOLoop` instance when one already exists, expecting a `RuntimeError` to be raised.

### Bug Explanation:
- The bug occurs due to incorrect logic in the `initialize()` function.
- When `make_current=True` and there is already a current `IOLoop` instance (`IOLoop.current(instance=False) is not None`), the code mistakenly raises a `RuntimeError` stating "current IOLoop already exists".
- This contradicts the intended behavior as it should only raise an error if `make_current=True` and no current instance exists.

### Bug Fix Strategy:
- Modify the logic in the `initialize()` function to correctly handle the case when `make_current=True` and there is already a current `IOLoop` instance.
- Only raise a `RuntimeError` when trying to make the current instance if `make_current=True` and no current instance exists.

### Corrected Version:
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

With this corrected version, the `initialize()` function will now correctly handle the case when trying to make the current `IOLoop` instance with `make_current=True` and an existing current instance. This fix will ensure that the `RuntimeError` is only raised when necessary, aligning with the expected behavior in the failing test.