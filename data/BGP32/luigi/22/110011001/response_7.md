### Bug Explanation
The error message `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` indicates that the variable `self.last_active` is of type `NoneType` when it should be an integer representing the seconds since epoch. The issue arises because the `last_active` parameter in the `__init__` function is set to `None` by default if no value is provided during object instantiation. This default value should be handled properly to avoid this type mismatch.

### Bug Fix Strategy
To fix this bug, you should check if `last_active` is `None` during object creation and assign the current time (seconds since epoch) if it is. This ensures that `last_active` always contains an integer value and avoids the `NoneType` mismatch error.

### Corrected Version
```python
class Worker(object):
    """
    Structure for tracking worker activity and keeping their references.
    """

    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
        if last_active is None:
            last_active = time.time()  # set current time if last_active is not provided
        self.last_active = last_active  # seconds since epoch
        self.started = time.time()  # seconds since epoch
        self.tasks = set()  # task objects
        self.info = {}
```

By making this change, the `last_active` parameter will default to the current time if not provided, ensuring that it is always an integer value representing seconds since epoch. This correction should resolve the `TypeError` and fix the bug.