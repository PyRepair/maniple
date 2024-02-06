The issue is occurring in the `initialize` method of the `IOLoop` class. When `make_current` is `True`, the method is checking if the current IOLoop exists, and if it does, it raises a `RuntimeError` with the message "current IOLoop already exists". However, the logic seems incorrect as it's raising the error when the current IOLoop exists, which is contradictory to the error message.

To fix this issue, we need to adjust the logic to raise the `RuntimeError` only when the current IOLoop does not exist and `make_current` is `True`. If `make_current` is `False` or `None`, it should not attempt to make the IOLoop current.

The corrected code for the `initialize` method is as follows:

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

This fix ensures that the `RuntimeError` is raised only when `make_current` is `True` and the current IOLoop exists. Otherwise, it will either make the IOLoop current or do nothing based on the value of `make_current`.