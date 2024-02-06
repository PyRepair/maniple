The test case `test_force_current` in the file `tornado/test/ioloop_test.py` is trying to initialize a new `IOLoop` with `make_current=True`. The expected behavior is that if there is no current `IOLoop` instance, the new instance should become the current one. If there is already a current instance and `make_current=True`, it should raise a `RuntimeError`.

The error message indicates that the `current IOLoop already exists` error is being raised when trying to initialize a new `IOLoop` instance with `make_current=True`. This suggests that the condition for checking whether a current `IOLoop` exists is not working correctly.

Upon reviewing the `initialize` function of the `IOLoop` class, it seems that the condition for checking the existence of a current `IOLoop` is incorrect. The logic inside the `initialize` function should be revised to achieve the expected behavior.

To fix the bug, the condition for checking the existence of a current `IOLoop` needs to be updated. The condition `if IOLoop.current(instance=False) is None:` should be changed to `if IOLoop.current(instance=True) is None:` to check for the existence of a current instance. Additionally, the logic for handling the `make_current` parameter should be modified to ensure that the new instance becomes the current one when `make_current=True` and no current instance exists.

Here is the revised version of the `initialize` function that resolves the issue:

```python
def initialize(self, make_current=None):
    current_instance = IOLoop.current(instance=True)
    if make_current is None:
        if current_instance is None:
            self.make_current()
    elif make_current:
        if current_instance is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

With these changes, the logic will correctly handle the `make_current` parameter and ensure that the new `IOLoop` instance becomes the current one when appropriate.