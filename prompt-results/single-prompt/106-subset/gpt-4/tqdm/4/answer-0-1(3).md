I have identified the issue in the `format_meter` function. The problem is with the following block of code where it tries to apply the custom scale:

```python
if unit_scale and unit_scale not in (True, 1):
    total *= unit_scale
    # ...
```

In this case, since `total` is `None`, it raises a `TypeError`. To resolve this issue, we should check if `total` is not `None` before applying the custom scale. Here is the modified and fixed `format_meter` function:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    # ...

    # apply custom scale if necessary
    if unit_scale and unit_scale not in (True, 1):
        if total is not None:
            total *= unit_scale
        n *= unit_scale
        if rate:
            rate *= unit_scale  # by default rate = 1 / self.avg_time
        unit_scale = False
    # ...

```

This fix should resolve the test error without affecting any other successful tests in the original project. You can apply this patch to the original project to fix the issue.