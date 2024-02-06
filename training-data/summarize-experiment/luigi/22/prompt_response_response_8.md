```python
class Worker(object):
    """
    Structure for tracking worker activity and keeping their references.
    """

    def __init__(self, worker_id, last_active=None):
        # Set the id of the Worker to the provided worker_id
        self.id = worker_id
        self.reference = None
        # Set self.last_active to zero if last_active is None
        if last_active is None:
            self.last_active = 0
        else:
            self.last_active = last_active
        self.started = time.time()
        self.tasks = set()
        self.info = {}
```