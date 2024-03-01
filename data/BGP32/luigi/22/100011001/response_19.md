### Bug Explanation
In the `prune` method of the `Worker` class, there is a comparison involving `self.last_active` and `config.worker_disconnect_delay`. The error message indicates that the `TypeError` is occurring due to an unsupported operand type for the `+` operation, specifically between a `NoneType` and an `int`. This implies that `self.last_active` is `None`, which cannot be added to an integer value.

### Bug Fix Strategy
To fix this bug, we need to ensure that `self.last_active` is always initialized to a valid value, such as an integer representing seconds since epoch. One way to approach this is to provide a default value for `last_active` parameter in the constructor.

### Corrected Version of the Function
```python
def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    self.last_active = last_active if last_active is not None else time.time()  # seconds since epoch
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
``` 

By assigning `time.time()` to `self.last_active` when the `last_active` parameter is `None`, we ensure that there is always a valid value for `self.last_active`. This will prevent the `TypeError` when trying to add an integer to `None`.