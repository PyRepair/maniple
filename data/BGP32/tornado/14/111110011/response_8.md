### Analysis:
1. The `initialize` function in the `IOLoop` class is designed to either make the current `IOLoop` instance automatically or check if it already exists depending on the `make_current` parameter.
2. The bug occurs when the `make_current` parameter is set to `True` and the current instance is not `None`, which results in a `RuntimeError` being raised incorrectly.
3. The failing test `test_force_current` tries to create a new instance with `make_current=True`, which should fail if an `IOLoop` instance already exists.
4. The bug happens because the condition to check if an `IOLoop` instance is already existing is incorrect. It should only raise an error if `make_current` is explicitly set to `True` and the current instance is not `None`.
5. To fix the bug, we need to adjust the logic in the `initialize` function to correctly handle the case when `make_current=True` and an `IOLoop` instance already exists.

### Bug Fix:
Here is the corrected version of the `initialize` function:

```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current() is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By changing the condition `IOLoop.current(instance=False) is None` with `IOLoop.current() is not None` in the `elif` block, we fix the bug related to checking if an `IOLoop` instance already exists correctly.

This correction ensures that the `RuntimeError` is raised only when `make_current=True` and there is already an existing `IOLoop` instance.

This fix should now resolve the issue reported on GitHub and make the failing test `test_force_current` pass successfully.