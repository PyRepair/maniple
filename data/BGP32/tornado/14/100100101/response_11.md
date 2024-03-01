### Analysis
The `initialize` function in the `IOLoop` class is supposed to handle the initialization of an `IOLoop` instance, including making it the current `IOLoop`. The bug in the function is related to the logic for handling the `make_current` parameter. The issue arises when trying to create a new `IOLoop` instance with `make_current=True` when there is already a current `IOLoop` instance.

### Error Location
The bug is located in the `initialize` function when checking if a current `IOLoop` instance exists before calling `self.make_current()`. The condition to raise a `RuntimeError` when `make_current=True` and a current `IOLoop` already exists is not being properly evaluated.

### Cause of the Bug
When the test function `test_force_current` is executed and attempts to create a new `IOLoop` instance with `make_current=True`, it fails to correctly raise a `RuntimeError` as expected when there is already a current `IOLoop` instance.

### Bug Fix Strategy
To fix the bug, the condition to raise a `RuntimeError` needs to be updated to accurately detect if a current `IOLoop` instance already exists when `make_current=True`.

### Corrected Version
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False):
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By updating the condition `if IOLoop.current(instance=False)` for raising a `RuntimeError`, the corrected version of the function should now correctly handle the scenario where a current `IOLoop` instance already exists.