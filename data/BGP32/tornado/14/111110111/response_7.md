### Bug Analysis:
1. The buggy function `initialize` in the `IOLoop` class is checking if `make_current` is `True` and then verifying if the current `IOLoop` instance exists. If it does not exist, it raises a `RuntimeError` stating that the current `IOLoop` already exists which is contradictory.
2. The test case `test_force_current` calls the `initialize` function with `make_current=True` and expects a new `IOLoop` instance to be created if the current instance does not exist.

### Bug Explanation:
1. The buggy function `initialize` checks if `make_current` is `True`, then checks if the current `IOLoop` instance is `None`. If it is not `None`, it raises a `RuntimeError` stating that the current `IOLoop` already exists, which contradicts the initial condition.
2. The failing test `test_force_current` tries to initialize a new `IOLoop` with `make_current=True` and expects the initialization to succeed even if the current instance exists, but it fails due to the contradictory condition in the `initialize` function.

### Bug Fix Strategy:
To fix the bug in the `initialize` function:
1. Remove the check that raises a `RuntimeError` if the current `IOLoop` instance exists when `make_current=True`.
2. If `make_current=True`, make the new `IOLoop` instance the current instance regardless of the existing instance.

### Corrected Version of the Function:
```python
class IOLoop(Configurable):
    
    # other functions here...

    def initialize(self, make_current=None):
        current_instance = IOLoop.current(instance=False)
        if make_current is None:
            if current_instance is None:
                self.make_current()
        elif make_current:
            if current_instance is None:
                self.make_current()
            else:
                self.make_current()
```

By modifying the `initialize` function as shown above, the new logic allows the creation of a new `IOLoop` instance with `make_current=True` regardless of the existence of the current instance. This change addresses the contradictory condition and ensures the test case `test_force_current` will pass as expected.