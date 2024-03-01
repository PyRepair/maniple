### Analysis
1. The `initialize` function in the `IOLoop` class is designed to initialize an instance of the `IOLoop` class, potentially making it the current `IOLoop` instance if specified.
2. The bug in the code occurs when `make_current=True` and there is already a current `IOLoop` instance, but the function still tries to make the new instance current, leading to a `RuntimeError`.
3. The failing test `test_force_current` checks if the `IOLoop` instance creation with `make_current=True` correctly handles the scenario where there is already a current `IOLoop` instance.
4. To fix the bug, we need to ensure that when `make_current=True` and there is already a current `IOLoop` instance, a `RuntimeError` is raised as indicated in the failing test.

### Fix
```python
class IOLoop(Configurable):
    # existing class code

    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:  # Check if current IOLoop already exists
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

By modifying the condition from `if IOLoop.current(instance=False) is None:` to `if IOLoop.current(instance=False) is not None:`, we ensure that if there is already a current `IOLoop` instance and `make_current=True`, a `RuntimeError` will be raised, as expected in the failing test.