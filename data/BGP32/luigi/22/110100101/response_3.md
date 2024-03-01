## Bug Explanation
The bug in the `__init__` function of the `Worker` class is that the `last_active` parameter is not being assigned correctly. The `last_active` parameter is being assigned directly to `self.last_active`, but it should be checked if it is `None` in order to set the current timestamp when the worker was last active.

## Bug Fix
To fix the bug, we need to check if the `last_active` parameter is `None`. If it is `None`, we should set the current timestamp as the value of `self.last_active`. 

Here is the corrected version of the `__init__` function:

```python
class Worker(object):
    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None
        if last_active is None:
            self.last_active = time.time()
        else:
            self.last_active = last_active
        self.started = time.time()
        self.tasks = set()
        self.info = {}
```

By making this change, the `last_active` parameter will be correctly handled during the initialization of a `Worker` instance.

This corrected version will pass the failing test case `test_worker_prune_after_init`.