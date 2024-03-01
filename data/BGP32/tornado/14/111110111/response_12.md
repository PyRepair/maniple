To fix the bug in the `initialize` function, we need to ensure that the check for an existing current `IOLoop` instance is correct. The current implementation checks if `IOLoop.current(instance=False)` is `None`, and if it is not `None`, it raises a `RuntimeError`. This is incorrect because the expected behavior is to raise an error if the current instance exists when `make_current` is set to `True`.

To address this issue, we should modify the logic to only raise an error if `make_current` is set to `True` and there is already a current `IOLoop` instance.

Here is the corrected version of the `initialize` function:

```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

With this modification, the `initialize` function will correctly check if a current `IOLoop` instance already exists only when `make_current` is set to `True`. This change ensures that the function behavior aligns with the expected logic described.

After applying this correction, the failing test `test_force_current` should pass without raising a `RuntimeError`.