Your task is to assist a developer in analyzing a GitHub issue to identify a bug in a program. You will receive the source code of the function suspected to contain the bug, along with associated GitHub issue. Your role is not to fix the bug but to summarize how the function implementation contributes to the faulty behaviour described in the issue. You summary needs to be a single paragraph; it must refer to concrete details from the issue description.

# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/scheduler.py



    # this is the buggy function you need to fix
    def __init__(self, worker_id, last_active=None):
        self.id = worker_id
        self.reference = None  # reference to the worker in the real world. (Currently a dict containing just the host)
        self.last_active = last_active  # seconds since epoch
        self.started = time.time()  # seconds since epoch
        self.tasks = set()  # task objects
        self.info = {}
    
```

