### Analysis
1. The `initialize` function in the `IOLoop` class is supposed to initialize the `IOLoop`, making it the current `IOLoop` if `make_current=True`.
2. The bug occurs because the function checks if there is already a current `IOLoop` instance before trying to make the new `IOLoop` current, but it does not handle the case where `make_current=True` and there is already a current instance. This leads to the `RuntimeError: current IOLoop already exists` error.
3. The failing test `test_force_current` tries to create a new `IOLoop` instance with `make_current=True`, then attempts to create a second instance with `make_current=True` which should fail.
4. To fix the bug, we need to check if there is already a current `IOLoop` instance before making a new `IOLoop` current when `make_current=True`.
5. The corrected version of the function is provided below.

### Corrected Version
```python
class IOLoop(Configurable):
    ...

    def initialize(self, make_current=None):
        current_instance = IOLoop.current(instance=False)
        
        if make_current is None:
            if current_instance is None:
                self.make_current()
        elif make_current:
            if current_instance is not None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
``` 

By updating the `initialize` function to check for the current instance before attempting to make a new instance current, we can prevent the `RuntimeError` from occurring. The corrected function should pass the failing test.