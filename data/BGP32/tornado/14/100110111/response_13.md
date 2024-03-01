### Analysis:
1. The buggy function `initialize` in the `tornado/ioloop.py` file is designed to initialize the `IOLoop` object with an optional parameter `make_current`.
2. The failing test `test_force_current` in `tornado/test/ioloop_test.py` constructs two `IOLoop` objects with `make_current=True`, expecting a `RuntimeError` to be raised on the second construction.
3. The failing test triggers an `RuntimeError: current IOLoop already exists` because the function does not handle the scenario where `make_current` is `True` and `IOLoop.current()` already exists.
4. To fix this bug, we need to modify the logic inside the `initialize` function to check whether an `IOLoop` instance already exists before creating a new one.

### Bug Explanation:
In the failing test `test_force_current`:
- The first `IOLoop` object is created with `make_current=True`.
- The second `IOLoop` object is then created also with `make_current=True`, which triggers the `RuntimeError` because the function does not handle the case where `make_current=True` and an `IOLoop` instance already exists.

### Bug Fix Strategy:
To fix the bug:
- We should modify the `initialize` function to check if an `IOLoop` instance already exists before creating a new one with `make_current=True`.
- If an `IOLoop` instance already exists and `make_current=True`, then we should raise a `RuntimeError`.

### The Corrected Version:
```python
def initialize(self, make_current=None):
    current_loop = IOLoop.current(instance=False)
    if make_current is None:
        if current_loop is None:
            self.make_current()
    elif make_current:
        if current_loop is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

By making the above changes, the corrected function should now pass the failing test `test_force_current` and handle the scenario where an `IOLoop` instance already exists with `make_current=True`.