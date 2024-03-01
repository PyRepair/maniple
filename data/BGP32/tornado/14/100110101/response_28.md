### Analysis
The buggy function `initialize` checks if an IOLoop instance already exists and raises a `RuntimeError` if `make_current` is `True` and there is already an existing IOLoop instance. The failing test `test_force_current` creates an IOLoop instance with `make_current=True`, expects it to be the current IOLoop, and then tries to create another IOLoop instance with `make_current=True`, expecting it to raise a `RuntimeError`.

### Bug
The bug occurs because the `initialize` function does not correctly handle the case when `make_current=True` and there is already an existing IOLoop instance. It should throw a `RuntimeError` only when `make_current` is `True` and there is an existing IOLoop instance.

### Fix
To fix the bug, we need to modify the logic in the `initialize` function to correctly check if an IOLoop instance already exists when `make_current=True`. We should only raise a `RuntimeError` in this scenario.

### Corrected Function
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