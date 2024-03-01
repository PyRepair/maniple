### Analysis
The error occurs because `self.last_active` is initialized as `None`, and when trying to add an integer to `None`, a `TypeError` is raised. The bug happens due to the comparison operation involving `None` in the `prune` method.

### Fix
Initialize `self.last_active` with the current time in seconds since epoch if it is `None`, before performing any comparisons.

### Corrected Version
```python
import time

def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    self.last_active = last_active if last_active is not None else time.time()  # seconds since epoch
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
```