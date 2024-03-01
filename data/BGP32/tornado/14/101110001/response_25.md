### Analysis:
1. The buggy function `initialize` in the `IOLoop` class checks if an instance of `IOLoop` already exists before making it the current instance.
2. The failing test `test_force_current` tries to create a new `IOLoop` instance with `make_current=True`, but the buggy function is incorrectly checking for an existing instance.
3. The error message indicates that the check for an existing instance is not working as expected, leading to the RuntimeError.
4. To fix the bug, the function needs to be modified to correctly handle the case when an existing instance is already set as the current one.

### Bug Fix Strategy:
1. Update the `initialize` function to correctly check for an existing current instance of `IOLoop` before making a new one the current instance.
2. If `make_current=True` is specified and an existing instance is already set, raise a RuntimeError.

### Corrected Version:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if self.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if self.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By making this change, the corrected version of the function should now pass the failing test without throwing a RuntimeError.