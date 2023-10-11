```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if self.__class__.instance() is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

Explanation:
The issue with the original code is that when `make_current` is `None` or `True`, it checks if `IOLoop.current(instance=False)` is `None`. If it is `None`, it raises a `RuntimeError` with the message "current IOLoop already exists", which is incorrect.

To fix the issue, we need to change the condition in the `elif` block. Instead of checking `IOLoop.current(instance=False)`, we should check `self.__class__.instance()`. The `instance()` method returns the current instance of the `IOLoop` class, and if it is not `None`, we raise the `RuntimeError`.

Additionally, we should call `self.make_current()` in both the `if` and `elif` blocks to ensure that the current instance is set properly.

The updated code snippet fixes the bug and ensures that the tests pass without affecting other successful tests.