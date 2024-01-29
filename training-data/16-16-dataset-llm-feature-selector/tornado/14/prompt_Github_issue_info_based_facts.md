# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
def initialize(self, make_current=None):
    if make_current is None:
        if IOLoop.current(instance=False) is None:
            self.make_current()
    elif make_current:
        if IOLoop.current(instance=False) is None:
            raise RuntimeError("current IOLoop already exists")
        self.make_current()

```

The github issue message is:
# A GitHub issue title for this bug
```text
ioloop.py(line 252) is None or not None
```

## The associated detailed issue description
```text
line 252, IOLoop.current(instance=False) is None。why then raise "already exists"?
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


