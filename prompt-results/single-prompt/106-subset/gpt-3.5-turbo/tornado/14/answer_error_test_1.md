```
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current and IOLoop.current(instance=False) is not None:
        raise RuntimeError("current IOLoop already exists")
    elif make_current:
        self.make_current()
```