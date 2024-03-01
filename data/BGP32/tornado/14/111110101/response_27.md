### Analysis
1. The `initialize` function in the `IOLoop` class is intended to initialize the IOLoop instance, and if `make_current` is `True`, it should ensure that there is not already a current instance before making itself the current instance.
2. The bug occurs when `make_current` is `True`, and it checks if there is no current instance by calling `IOLoop.current(instance=False)`. This check is incorrect as it does not correctly determine the absence of a current instance.
3. The failing test `test_force_current` expects that when `make_current` is set to `True`, the initialization should raise a `RuntimeError` if there is already a current instance.
4. To fix the bug, we need to adjust the check for the presence of a current instance and correctly handle the scenario when `make_current` is `True`.

### Bug Fix Strategy
1. Modify the logic in the `initialize` function to accurately check for the existence of a current instance when `make_current` is set to `True`.
2. If `make_current` is `True`, first check if there is a current instance, if yes, raise `RuntimeError`, otherwise make the current instance.
3. Update the code to properly handle the scenario when `make_current` is `True`.

### Corrected Code
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=True) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```