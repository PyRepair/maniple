The bug in the provided code is that when the `last_active` parameter is not provided, it defaults to `None`, but it should default to the current time in seconds since epoch.

### Strategy for fixing the bug:
To fix the bug, we need to modify the initialization of `last_active` in the `__init__` function to set it to the current time if no value is provided.

### Corrected version of the function:
```python
import time

class Worker(object):
    """
    Structure for tracking worker activity and keeping their references.
    """

    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
        self.last_active = last_active if last_active is not None else time.time()  # seconds since epoch
        self.started = time.time()  # seconds since epoch
        self.tasks = set()  # task objects
        self.info = {}
``` 

Now, the `last_active` parameter in the `__init__` function will default to the current time if no value is provided, ensuring that the expected values and types of variables are met in all cases.