### Explanation:
- The buggy function `initialize` in the `IOLoop` class is responsible for initializing the IOLoop object. The bug occurs when `make_current=True` is passed as an argument.
- The issue arises because the code checks if `IOLoop.current(instance=False)` is None, and if it is not None, it raises a `RuntimeError` stating "current IOLoop already exists". This logic is incorrect because if `IOLoop.current(instance=False)` is not None, it should not raise an error.
- The failing test `test_force_current` tries to create an `IOLoop` with `make_current=True` and expects it to be the current `IOLoop` instance. It then attempts to create a second `IOLoop` with `make_current=True`, which should fail since there can only be one current instance.

### Bug Fix Strategy:
- Modify the logic in the `initialize` function to only raise a `RuntimeError` if `make_current` is `True` and there is already a current `IOLoop` instance.
- Update the condition to check if `make_current` is `True` and if `IOLoop.current(instance=False)` is not None.
- Remove the unnecessary check for `IOLoop.current(instance=False)` being None when `make_current=None`.

### Corrected Version:
```python
def initialize(self, make_current=None):
    if make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("Current IOLoop already exists")
        self.make_current()
    elif make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
```

By fixing the logic in the `initialize` function as shown above, the issue should be resolved, and the corrected version should pass the failing test.