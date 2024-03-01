This bug is related to the `initialize` method of the `IOLoop` class in the `tornado/ioloop.py` file. The issue occurs when trying to force the current `IOLoop` instance to be created. The failing test `test_force_current` expects that when attempting to create a new `IOLoop` instance with `make_current=True`, it should raise a `RuntimeError` if an `IOLoop` instance already exists.

The bug occurs because in the `initialize` method, the validation check for the current `IOLoop` instance is incorrect. The logic in the `if` statement should be inverted. It should raise a `RuntimeError` when `make_current=True` and an `IOLoop` instance already exists.

Here is the corrected version of the `initialize` method:

```python
# The relative path of the corrected file: tornado/ioloop.py

def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By making this change, the `initialize` method will now correctly raise a `RuntimeError` when attempting to force the creation of a new `IOLoop` instance while one already exists. This correction aligns with the expected behavior in the failing test case and resolves the issue reported on GitHub.