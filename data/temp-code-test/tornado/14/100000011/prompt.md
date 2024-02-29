Please fix the buggy function provided below and output a corrected version.
Following these steps:
1. Analyze the buggy function and its relationship with the GitHub issue.
2. Identify potential error locations within the buggy function.
3. Explain the cause of the bug using the buggy function, the GitHub Issue information.
4. Suggest a strategy for fixing the bug.
5. Given the buggy function below, provide a corrected version. The corrected version should resolve the issue posted in GitHub.


## The source code of the buggy function
```python
# The relative path of the buggy file: tornado/ioloop.py

# this is the buggy function you need to fix
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()

```




## A GitHub issue for this bug

The issue's title:
```text
ioloop.py(line 252) is None or not None
```

The issue's detailed description:
```text
line 252, IOLoop.current(instance=False) is None。why then raise "already exists"?
```



