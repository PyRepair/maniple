### Analysis:
1. The buggy function `initialize` in the `IOLoop` class is checking if an `IOLoop` instance already exists before making the current `IOLoop` instance. If `make_current=None`, it checks if there is no current instance and then calls `make_current()`. If `make_current=True`, it checks if there is already a current instance and raises an error if so.
   
2. The failing test `test_force_current` tries to create a new `IOLoop` instance with `make_current=True`, expecting that it should raise a `RuntimeError` if a current `IOLoop` instance already exists.

3. The bug occurs because when `make_current=True`, the function first checks if `IOLoop.current(instance=False)` is None, and if it is not None (indicating a current instance exists), it still tries to set the current instance which causes the `RuntimeError`.

4. To fix the bug, the function should only try to set the current instance when `make_current=True` if there is no current instance already present.

### Bug Fix:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:  # Check if current IOLoop exists
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By updating the condition in the `elif` block to check if `IOLoop.current(instance=False)` is not None, we ensure that the `RuntimeError` is only raised when a current instance exists, as intended.

This fix should resolve the bug and pass the failing test `test_force_current`.