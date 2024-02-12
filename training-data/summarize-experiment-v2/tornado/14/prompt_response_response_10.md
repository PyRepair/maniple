```python
    def initialize(self, make_current=None):
        current_ioloop = IOLoop.current(instance=False)
        
        if make_current is None:
            if current_ioloop is None:
                self.make_current()
        elif make_current:
            if current_ioloop is not None:
                raise RuntimeError("current IOLoop already exists")
            self.make_current()
```