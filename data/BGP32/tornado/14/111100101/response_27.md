## Analysis
1. The `initialize` function checks the `make_current` parameter and if it is `None`, it checks if there is no current instance of `IOLoop`. If there is none, it calls the `make_current` function. If `make_current` is `True`, it checks if there is a current instance of `IOLoop`, and if not, raises a `RuntimeError`.
2. The failing test `test_force_current` creates an instance of `IOLoop` with `make_current=True`, expects it to be the current instance, then tries to create another instance with `make_current=True`, which should raise a `RuntimeError`.
3. The bug occurs in the logic checking for an existing current instance of `IOLoop`.
4. The bug is caused by not properly handling the case where `make_current` is `True` and there is no current instance of `IOLoop`.
5. To fix the bug, we need to modify the logic in the `initialize` function to properly check for the presence of a current instance when `make_current` is `True`.

## Bug Fix
```python
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