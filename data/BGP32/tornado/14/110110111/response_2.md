To fix the bug in the `initialize` function of the `IOLoop` class, we need to correct the logic for checking if a current `IOLoop` instance exists. The issue stems from the improper handling of the `make_current` parameter, leading to an incorrect check for the existence of the current `IOLoop`.

### Bug Explanation:
In the buggy function `initialize`, when `make_current` is `True`, the code is checking if there is no current instance of `IOLoop` before calling `self.make_current()`. However, if the check is successful (no current instance is found), it erroneously raises a `RuntimeError` stating "current IOLoop already exists".

The expected behavior, as per the test case provided, is to raise a `RuntimeError` only when a current `IOLoop` instance already exists and `make_current` is set to `True`.

### Fix Strategy:
1. Check if `make_current` is `True` and there is already a current instance of `IOLoop`.
2. If there is no current instance of `IOLoop` and `make_current` is `True`, then proceed to make the current `IOLoop`.

### Corrected Version:
```python
class IOLoop(Configurable):

    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

With this corrected version, the `initialize` function will correctly handle the case when `make_current` is `True`, ensuring that a `RuntimeError` is only raised when a current instance of `IOLoop` already exists.