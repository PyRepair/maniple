```python
class Worker(object):
    """
    Structure for tracking worker activity and keeping their references.
    """

    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None
        if last_active is None:
            self.last_active = 0  # Set self.last_active to zero if last_active is None
        else:
            self.last_active = last_active
        self.started = time.time()
        self.tasks = set()
        self.info = {}
```