### Analysis:
1. The buggy function `initialize` has an issue when `make_current` is True. It should raise a `RuntimeError` if there is already a current IOLoop instance.
2. The failing test `test_force_current` tries to create a new IOLoop instance with `make_current=True`, which should fail and raise a `RuntimeError`.

### Bug Explanation:
The bug is in the `initialize` function where it should raise a `RuntimeError` only if `make_current` is True and there is already a current IOLoop instance. However, it does not correctly handle this scenario and allows the creation of duplicate current instances.

### Bug Fix:
To fix the bug, we need to modify the `initialize` function to raise a `RuntimeError` only when `make_current` is True and there is already a current IOLoop instance.

### Corrected Function:
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

After applying the fix, the `initialize` function will correctly handle the scenario when `make_current=True` and there is already a current IOLoop instance.