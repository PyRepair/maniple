### Analysis:
1. The `initialize` function in `tornado/ioloop.py` is supposed to initialize the IOLoop instance, but it has a bug where it incorrectly handles the `make_current` parameter.
2. The failing test `test_force_current` in `tornado/test/ioloop_test.py` creates an IOLoop instance with `make_current=True` and then attempts to create another one with the same parameter, expecting it to raise a `RuntimeError`, which is not happening.
3. The GitHub issue points out the inconsistency where the `initialize` function checks if the current IOLoop is `None` before raising the `already exists` error, which does not align with the implementation logic.
4. To fix the bug, we need to ensure that if `make_current=True` is passed and there is already an existing IOLoop instance, a `RuntimeError` should be raised immediately without checking if it is `None` or not.

### Bug Fix:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:  # Change from None to not None
            raise RuntimeError("current IOLoop already exists")  # Raise error immediately if IOLoop already exists
        self.make_current()
```

By making this change, the `initialize` function will work correctly as expected. It will now raise a `RuntimeError` if `make_current=True` is passed and there is an existing IOLoop instance. This will fix the bug and make the failing test `test_force_current` pass successfully.