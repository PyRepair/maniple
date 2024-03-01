### Bug Explanation
The error message `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` indicates that there is an issue with using `NoneType` in the addition operation in the `prune` method of the `Worker` class. Specifically, the `last_active` attribute is being initialized as `None`, and when trying to add an `int` value to `None`, it results in a `TypeError`.

### Bug Fix Strategy
To fix this bug, we need to ensure that `last_active` is initialized with a proper value if `last_active` is not provided. We can set a default value of `0` for `last_active` if no value is passed during initialization.

### Corrected Version
```python
def __init__(self, worker_id, last_active=None):
    self.id = worker_id
    self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
    self.last_active = last_active if last_active is not None else 0  # seconds since epoch or default to 0
    self.started = time.time()  # seconds since epoch
    self.tasks = set()  # task objects
    self.info = {}
``` 

By initializing `last_active` with `0` if `last_active` is `None`, we ensure that addition operations work as expected without raising any `TypeError` due to combining incompatible types.