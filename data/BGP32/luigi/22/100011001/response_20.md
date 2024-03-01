### Explanation:
The error message indicates that there is a `TypeError` when trying to add `self.last_active` (which is of type `NoneType`) to an integer value. This occurs at the line `if self.last_active + config.worker_disconnect_delay < time.time():`.

### Bug cause:
The `last_active` parameter in the `__init__` function is set to `None` by default and is not properly handled when trying to calculate the worker's active time later in the code.

### Fix strategy:
Ensure that `last_active` is initialized to a valid value when not provided by the user, so it can be used in the calculation later in the code without causing a `TypeError`.

### Corrected version:
```python
def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    self.last_active = last_active if last_active is not None else time.time()  # seconds since epoch
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
``` 

By ensuring that `last_active` is set to the current time if not provided, we avoid the `TypeError` when using it in the `prune` method.