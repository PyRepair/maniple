To fix the bug in the `initialize` function, we need to update the condition to check if an instance of `IOLoop` already exists when `make_current=True`. The current implementation raises an error even when no instance exists, which is incorrect. We need to adjust the logic to only raise an error if an instance already exists.

Here is the corrected version of the `initialize` function:

```python
class IOLoop(Configurable):
    ...
    
    def initialize(self, make_current=None):
        if make_current is None:
            if IOLoop.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if IOLoop.current(instance=False) is not None:  # Changed condition
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```

By changing the condition from `if IOLoop.current(instance=False) is None` to `if IOLoop.current(instance=False) is not None`, we ensure that the error is only raised when an instance already exists, which aligns with the expected behavior.

This correction should resolve the issue reported on GitHub and make the function pass the failing test case.