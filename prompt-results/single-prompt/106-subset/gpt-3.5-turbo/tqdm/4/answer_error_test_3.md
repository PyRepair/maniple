To fix the bug, you can replace the line `total *= unit_scale` with the following lines of code:

```
if total is not None:
    total *= unit_scale
```

Here's the fixed code snippet:

```python
@staticmethod
def format_meter(n,