### Bug Explanation
The bug in the `__init__` function of the `Worker` class is related to the incorrect handling of the `last_active` parameter. The `last_active` parameter is intended to take a value in seconds since epoch, but the bug causes it to be set incorrectly. This results in unexpected behavior when creating a new `Worker` instance and trying to prune it.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `last_active` parameter is correctly assigned to the `last_active` attribute of the `Worker` instance.

### Corrected Version
```python
def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    self.last_active = last_active if last_active is not None else time.time()  # seconds since epoch
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
``` 

By making this correction, the `last_active` parameter will be correctly assigned to the `last_active` attribute of the `Worker` instance, ensuring that the behavior is as expected when creating and pruning workers.