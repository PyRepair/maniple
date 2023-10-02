To fix the error, you need to modify the `format_meter` function by adding a condition to check if `total` is not `None` before multiplying it with `unit_scale`. Here's the complete fixed code:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    # ... comments ...

    # sanity check: total
    if total and n > total:
        total = None

    # apply custom scale if necessary
    if unit_scale and unit_scale not in (True, 1):
        if total is not None:
            total *= unit_scale
        n *= unit_scale
        if rate:
            rate *= unit_scale  # by default rate = 1 / self.avg_time
        unit_scale = False
    # ... rest of the code ...
```
