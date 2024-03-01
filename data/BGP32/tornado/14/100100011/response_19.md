### Analysis:
1. The `initialize` function has conditional checks based on the `make_current` parameter, ensuring that only one current `IOLoop` instance exists.
2. The failing test `test_force_current` tries to create multiple `IOLoop` instances with `make_current=True`, expecting a `RuntimeError` when trying to create a second instance.
3. The `initialize` function logic is intended to prevent the creation of multiple current `IOLoop` instances, but the current implementation is not handling the case when trying to create a second instance correctly.
4. The bug occurs when the `initialize` function incorrectly raises a `RuntimeError` when trying to create a second current `IOLoop` instance, even though the first one does not exist.
### Bug Cause:
The bug in the `initialize` function occurs due to the incorrect handling of the case where the first `current` instance does not exist. The logic incorrectly raises an error when it should allow creating a new `IOLoop` instance in this scenario.
### Bug Fix:
To fix the bug, we need to modify the `initialize` function to correctly handle the case when the first current `IOLoop` instance does not exist. We should only raise a `RuntimeError` if there is already an existing current `IOLoop` instance when `make_current=True`.
### Corrected Version:
```python
def initialize(self, make_current=None):
    current_instance = IOLoop.current(instance=False)
    
    if make_current is None:
        if current_instance is None:
            self.make_current()
    elif make_current:
        if current_instance:
            raise RuntimeError("Current IOLoop already exists")
        self.make_current()
```
### Summary:
The corrected `initialize` function will now properly handle the case where a current `IOLoop` instance does not exist and only raise a `RuntimeError` when trying to create a second instance while the first one already exists. This fix should resolve the bug and make the failing test `test_force_current` pass successfully.