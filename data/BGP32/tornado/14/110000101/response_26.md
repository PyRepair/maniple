The buggy function `initialize` is meant to handle the initialization of an `IOLoop` instance, setting it as the current `IOLoop` if necessary based on the `make_current` parameter. However, there are issues in the logic implemented in the function.

### Bug explanation:
1. The logic for handling the `make_current` parameter is incorrect. In the case where `make_current` is True, the function checks if a current `IOLoop` instance exists and then calls `self.make_current()`. However, if a current instance does not exist, it should raise an error immediately rather than trying to make it current and then raising an error.
2. Additionally, the logic for the `make_current=None` case is problematic. It checks if there is no current instance and then calls `self.make_current()`. However, the `self.make_current()` method is not defined within the `IOLoop` class.

### Strategy for fixing the bug:
1. Update the logic for the `make_current=True` case to raise an error immediately if there is no current `IOLoop` instance.
2. Remove the incorrect call to `self.make_current()` and implement the necessary logic within the `IOLoop` class to handle making the instance current.

### Corrected version of the function:

```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            raise RuntimeError("Cannot make current: current IOLoop does not exist")
    elif make_current:
        if IOLoop.current(instance=False) is None:
            raise RuntimeError("Cannot make current: current IOLoop does not exist")
        self.make_current()
```