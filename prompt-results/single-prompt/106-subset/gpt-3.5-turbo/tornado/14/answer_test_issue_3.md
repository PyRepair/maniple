```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=True) is None:
            self.make_current()
        else:
            raise RuntimeError("current IOLoop already exists")
```