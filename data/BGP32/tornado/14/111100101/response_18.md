### Bug Analysis:
1. The `initialize` function in the `IOLoop` class is checking if `make_current` is `True` and there is no current instance of `IOLoop`, then it raises a `RuntimeError`. 
2. However, in the failing test `test_force_current`, the test creates an `IOLoop` instance with `make_current=True`, then tries to create another `IOLoop` instance with `make_current=True` again, which should raise a `RuntimeError`.
3. The bug is that the function does not prevent the creation of a new instance when `make_current=True` and a current instance already exists.

### Bug Fix Strategy:
To fix this bug, we need to check if `make_current=True` and there is already a current instance of `IOLoop`, then raise a `RuntimeError` to prevent the creation of a new instance.

### Corrected Function:
```python
class IOLoop(Configurable):
    # other functions unchanged
    
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