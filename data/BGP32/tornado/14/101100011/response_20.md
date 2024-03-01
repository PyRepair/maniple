### Analysis:
1. The `initialize` function in the `IOLoop` class checks if a current `IOLoop` instance exists before creating a new one.
2. The test function `test_force_current` initializes an `IOLoop` instance with `make_current=True` and then tries to create another one, expecting a `RuntimeError` to be raised.
3. The GitHub issue points out a discrepancy between the `None` check and the error message "current IOLoop already exists".

### Error Location:
- In the `initialize` function, the condition `if make_current is None` checks if there is no `IOLoop` instance already existing, but the subsequent code does not reflect the correct logic for handling this case.

### Cause of the Bug:
- The bug arises because even if `IOLoop.current(instance=False)` returns `None`, the code incorrectly proceeds to create a new `IOLoop` instance instead of raising an error as expected.

### Strategy for Fixing the Bug:
- Update the logic in the `initialize` function to correctly handle the case where `IOLoop.current(instance=False)` returns `None` when `make_current` is `None`.

### Corrected Version:
```python
    def initialize(self, make_current=None):
        current_instance = IOLoop.current(instance=False)
        if make_current is None:
            if current_instance is None:
                self.make_current()
        elif make_current:
            if current_instance is not None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

After applying this correction, the `initialize` function will correctly handle the case where no current `IOLoop` instance exists when `make_current` is `None`, preventing the creation of a duplicate instance.