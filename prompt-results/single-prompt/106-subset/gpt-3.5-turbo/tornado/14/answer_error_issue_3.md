```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current() is None:
            self.make_current()
    elif make_current:
        if IOLoop.current() is not None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()
```

Explanation:
The original code has an error in line 252, where it checks if `IOLoop.current() is None`, but then raises an error saying "current IOLoop already exists". To fix this, we should change the conditions in both branches of the if-else statement. In the first branch, we should check if `IOLoop.current()` is not None, and in the second branch, we should check if `IOLoop.current()` is None. This way, the code will only raise an error if `IOLoop.current()` is not None and `make_current=True`.

Note: In the fixed code, I have removed the `instance=False` argument from the `IOLoop.current()` calls because by default `instance=True` and we want to obtain the current IOLoop instance.