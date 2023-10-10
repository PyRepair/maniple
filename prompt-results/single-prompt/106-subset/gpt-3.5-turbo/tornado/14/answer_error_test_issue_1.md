```python
def initialize(self, make_current=None):
    if IOLoop.current(instance=False) is not None:
        raise RuntimeError("current IOLoop already exists")
       
    if make_current is None or make_current:
        self.make_current()
```
The issue is occurring because the current IOLoop check should be done at the beginning of the method, and if a current IOLoop instance exists, it should raise a RuntimeError. Additionally, the if statement checking if `make_current` is `None` should also check if `make_current` is `True` and only then call `self.make_current()`. This fix ensures that the program is correctly checking for the existence of a current IOLoop before making a new one and throwing the appropriate error message.