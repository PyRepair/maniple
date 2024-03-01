### Analyzing the buggy function

**Buggy class**: `IOLoop` 

**Buggy function**: `initialize(self, make_current=None)`

**Test code**: `test_force_current`

**Error message**: `RuntimeError: current IOLoop already exists`

**Expected input/output values**:
- When `make_current` is `True`, the function should raise a `RuntimeError` if the current `IOLoop` already exists.

### Bug Explanation
The bug occurs because the `initialize` function is checking if there is a current instance of the `IOLoop` before trying to make the current instance if `make_current` is not provided. If `make_current=True`, the `initialize` function should raise a `RuntimeError` if there is already a current instance of the `IOLoop`. However, the current implementation is checking for the absence of a current instance and then attempting to make it current, leading to the incorrect behavior.

### Bug Fix Strategy
To solve the bug:
1. Check if `make_current` is `True` and if there is already a current instance of `IOLoop`. 
2. If there is a current instance and `make_current=True`, raise a `RuntimeError`.
3. If there is no current instance and `make_current=True`, update the current instance to the new `IOLoop`.

### Corrected Code
```python
def initialize(self, make_current=None):
    if make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
    
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
        else:
            self.make_current()
```