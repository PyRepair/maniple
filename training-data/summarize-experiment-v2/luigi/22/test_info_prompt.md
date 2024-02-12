Please analyze the provided error message on command line, test code, and buggy source code, then identify what stack frames or messages are closely related to the fault location and simplify the original error message.


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


# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/scheduler_test.py

    def test_worker_prune_after_init(self):
        worker = luigi.scheduler.Worker(123)

        class TmpCfg:
            def __init__(self):
                self.worker_disconnect_delay = 10

        worker.prune(TmpCfg())
```


## The error message from the failing test
```text
self = <scheduler_test.SchedulerTest testMethod=test_worker_prune_after_init>

    def test_worker_prune_after_init(self):
        worker = luigi.scheduler.Worker(123)
    
        class TmpCfg:
            def __init__(self):
                self.worker_disconnect_delay = 10
    
>       worker.prune(TmpCfg())

test/scheduler_test.py:108: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <luigi.scheduler.Worker object at 0x7f78d9aa2250>
config = <scheduler_test.SchedulerTest.test_worker_prune_after_init.<locals>.TmpCfg object at 0x7f78d9aa22e0>

    def prune(self, config):
        # Delete workers that haven't said anything for a while (probably killed)
>       if self.last_active + config.worker_disconnect_delay < time.time():
E       TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'

luigi/scheduler.py:245: TypeError

```