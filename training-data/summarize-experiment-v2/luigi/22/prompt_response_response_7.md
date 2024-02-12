The issue with the current implementation is that 'last_active' is initialized to 'None' when the 'Worker' object is being created, causing a TypeError when trying to perform arithmetic operations on it.

To fix this, we can initialize 'last_active' to the default value of 'None' and then update it when the worker becomes active. This can be done by adding a new method to update the 'last_active' attribute.

Here is the corrected code for the buggy function:

```python
import time

class Worker(object):
    """
    Structure for tracking worker activity and keeping their references.
    """

    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
        self.last_active = last_active  # seconds since epoch or None
        self.started = time.time()  # seconds since epoch
        self.tasks = set()  # task objects
        self.info = {}

    def update_last_active(self):
        self.last_active = time.time()
        
    def prune(self, config):
        if self.last_active is not None and self.last_active + config.worker_disconnect_delay < time.time():
            # prune the worker
            pass
```

With this correction, the 'last_active' attribute is initialized to 'None' by default, and can be updated using the 'update_last_active' method when the worker becomes active. The 'prune' method has also been updated to handle the case where 'last_active' is 'None' before performing arithmetic operations.