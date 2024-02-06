```python
def __init__(self, worker_id, last_active=None):
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
    
    # additional attributes and initialization can be added here if needed
```