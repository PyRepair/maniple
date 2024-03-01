## Analysis:
1. The `initialize` function in the `IOLoop` class is intended to initialize the IOLoop instance.
2. The test function `test_force_current` is trying to create an IOLoop instance with `make_current=True` and check if it raises a `RuntimeError` correctly.
3. The error message indicates that the `initialize` function is raising a `RuntimeError` when it shouldn't.
4. The bug is in the `initialize` function logic where it checks if the current IOLoop instance exists before creating a new one.

## Bug Cause:
The bug is caused by the logic in the `initialize` function incorrectly checking for the current IOLoop instance. The intention is to ensure that a new IOLoop instance is only created if one doesn't already exist. However, the check is flawed because it raises a `RuntimeError` if a current IOLoop instance exists, even if `make_current=True`.

## Bug Fix Strategy:
1. Modify the conditional logic in the `initialize` function to only raise a `RuntimeError` when `make_current` is explicitly set to `True`.
2. If `make_current` is `None`, create a new IOLoop instance only if one does not already exist.
3. If `make_current=False`, explicitly set the `current` IOLoop instance without checking for an existing instance.

## Corrected Version:
```python
def initialize(self, make_current=None):
    if make_current is None:
        # Create a new IOLoop instance only if one doesn't already exist
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        # Check if a current IOLoop instance already exists
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()

# Apply the corrected logic in the `initialize` function
```