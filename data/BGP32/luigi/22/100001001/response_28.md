### Explanation:
The bug in the provided code is that the `last_active` parameter is not correctly assigned to the `self.last_active` attribute in the `__init__` method. The `last_active` parameter is not being used to set the value of `self.last_active`, which results in `self.last_active` being `None` even when a value is provided as `last_active`.

### Strategy for fixing the bug:
To fix this bug, you need to assign the `last_active` parameter to the `self.last_active` attribute in the `__init__` method.

### Corrected version:

```python
def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    
    if last_active is not None:
        self.last_active = last_active
    else:
        self.last_active = time.time()  # seconds since epoch
    
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
``` 

By checking if `last_active` is not `None`, the corrected version correctly assigns the provided `last_active` value to `self.last_active`. If `last_active` is `None`, it defaults to the current time using `time.time()`.