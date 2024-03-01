### Analysis:
1. The `initialize` method in the `IOLoop` class is designed to control the current `IOLoop` instance. It checks if the `make_current` parameter is `True` and if there is already a current `IOLoop` instance, it should raise a `RuntimeError`.
2. The bug occurs when the `make_current=True` and there is already a current `IOLoop` instance, the method should raise the `RuntimeError` as expected but it fails to do so.
3. The failing test `test_force_current` expects that creating a new `IOLoop` instance with `make_current=True` when there is already an existing current instance should raise a `RuntimeError`.
4. The bug is that the code checks if `IOLoop.current()` is `None` before raising the `RuntimeError`, which should not be the case.

### Bug Fix Strategy:
Modify the `initialize` method to first check if `make_current` is `True`, then directly raise the `RuntimeError` if there is already a current `IOLoop` instance.

### Corrected Function:
```python
def initialize(self, make_current=None):
    if make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
``` 

By correcting the code in this way, the function will properly handle the case of attempting to create a new `IOLoop` instance with `make_current=True` when there is already an existing current instance.