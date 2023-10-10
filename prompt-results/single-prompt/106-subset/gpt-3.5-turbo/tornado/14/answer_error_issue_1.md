```python
def initialize(self, make_current=None):
    # Check if make_current is None
    if make_current is None:
        # Check if there is no current IOLoop instance
        if IOLoop.current(instance=False) is None:
            # Make current IOLoop
            self.make_current()
    # Check if make_current is True
    elif make_current:
        # Check if there is already a current IOLoop instance
        if IOLoop.current(instance=False) is not None:
            raise RuntimeError("current IOLoop already exists")
        # Make current IOLoop
        self.make_current()
```