The bug in the `initialize` method of the `IOLoop` class is that it raises a `RuntimeError` with the message "current IOLoop already exists" when `make_current` is set to `True`, even if `IOLoop.current(instance=False)` returns `None`. This behavior contradicts the logic in the code.

The issue stems from incorrect conditional checks based on the `make_current` parameter. The `initialize` method is supposed to ensure that only one current `IOLoop` instance exists when `make_current=True`.

To fix this bug, we need to update the conditional checks within the `initialize` method. The logic should be as follows:

1. When `make_current` is not provided:
   - If there is no current `IOLoop` instance, make the current instance.
   
2. When `make_current=True` is explicitly provided:
   - If there is no current `IOLoop` instance, make the current instance.
   - If there is already a current `IOLoop` instance, raise a `RuntimeError`.

Here is the corrected version of the `initialize` method:

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

This corrected version ensures that the `RuntimeError` is only raised when `make_current=True` and there is an existing current `IOLoop`.

By implementing this fix, the failing test case `test_force_current` should now pass successfully without raising an exception.