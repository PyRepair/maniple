## Explanation
The bug occurs because the `last_active` parameter has a default value of `None`, causing an error when trying to add it to `config.worker_disconnect_delay` which is an integer. This results in the `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`.

## Solution
To fix this bug, we need to ensure that `last_active` is always initialized with a default value in case it is not provided when creating a `Worker` object.

## Corrected code
```python
import time

class Worker:
    def __init__(self, worker_id, last_active=0):  # set a default value for last_active
        self.id = worker_id
        self.reference = None
        self.last_active = last_active
        self.started = time.time()
        self.tasks = set()
        self.info = {}

    def prune(self, config):
        if self.last_active + config.worker_disconnect_delay < time.time():
            # Do something here
            pass
```

By setting a default value of `0` for `last_active` in the `__init__` method, we ensure that it will always be initialized with a valid value. This change should fix the bug and make the test `test_worker_prune_after_init` pass.