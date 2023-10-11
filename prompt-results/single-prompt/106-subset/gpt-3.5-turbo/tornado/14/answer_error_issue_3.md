```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is not None:  # Fix: Check if current IOLoop exists
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

Explanation:
The bug occurs because in the `elif make_current:` branch, the code is checking if `IOLoop.current(instance=False)` is None, which means that there is no current IOLoop. But the error message raised is "current IOLoop already exists", which is contradictory. 

To fix this, we can replace the condition in line 5 with `if IOLoop.current(instance=False) is not None:`. This will check if a current IOLoop already exists and raise the exception if it does. Then, `self.make_current()` is always called after the check, ensuring that the IOLoop is made current when necessary.