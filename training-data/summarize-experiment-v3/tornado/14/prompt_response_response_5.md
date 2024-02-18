## Bug Cause
The bug likely stems from the conditional clause that checks if the current IOLoop instance is None, then raises a RuntimeError if make_current is set to True.

## Bug Fix
The conditional clause in the initialize function should be modified to properly handle the case when make_current is True and an IOLoop instance already exists.

## Corrected Code
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