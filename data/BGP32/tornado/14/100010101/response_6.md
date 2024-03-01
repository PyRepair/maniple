### Explanation
The buggy function `initialize` is intended to check if the `make_current` parameter is `True`, and if so, it should raise a `RuntimeError` if an IOLoop already exists. The bug occurs because the function does not correctly handle the case when `make_current` is `True` and an IOLoop already exists.

### Bug in the code
The bug occurs at line `if IOLoop.current(instance=False) is None:` which incorrectly checks if an IOLoop instance does not exist, leading to the wrong behavior when `make_current` is `True`.

### Fix strategy
To fix this bug, we need to modify the condition to check if an IOLoop instance already exists when `make_current` is `True`. If an IOLoop instance exists, then we should raise a `RuntimeError`. 

### Corrected code
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

After making this correction, the function should now correctly raise a `RuntimeError` if an IOLoop already exists and `make_current` is `True`.