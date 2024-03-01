### Analysis
- The function `initialize` is intended to initialize an `IOLoop` object, making it the current loop if specified.
- The bug occurs when `make_current` is `True` and the current `IOLoop` already exists, resulting in a `RuntimeError`.
- The error message indicates that the `current IOLoop already exists`.

### Bug Cause
- When `make_current` is `True`, the function incorrectly checks if the current `IOLoop` does not exist before trying to make it the current loop.
- This leads to an incorrect behavior where the function raises a `RuntimeError` even though it is instructed to make the loop current.

### Fix Strategy
- The fix involves only attempting to make the loop current if `make_current` is `True`, without checking if the loop already exists.

### Corrected Function
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        self.make_current()
``` 

With this correction, the function should correctly make the `IOLoop` current when `make_current` is `True` without checking if it already exists.