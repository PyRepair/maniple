The issue here appears to be that when `total` is `None`, the operation `total *= unit_scale` is attempting to perform a multiplication operation involving a `None` type which is not a valid operation.

Overriding the `None` value may lead to other issues as the `None` value likely carries some semantic value within the code. Instead, we can add checks before each operation involving `total` to ensure it is not `None`.

Here's the modified `format_meter` function:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    #...
    # apply custom scale if necessary
    if unit_scale and unit_scale not in (True, 1):
        if total is not None:  # Add check before operation
            total *= unit_scale
        n *= unit_scale
        if rate:
            rate *= unit_scale  # by default rate = 1 / self.avg_time
        unit_scale = False
    #...
    if total:
        # fractional and percentage progress
        if total is not None:  # Add check before operation
            frac = n / total
        else:
            frac = 0
            total = 0
        #...
    #...
    return ((prefix + ": ") if prefix else '') + \
        '{0}{1} [{2}, {3}{4}]'.format(
            n_fmt, unit, elapsed_str, rate_fmt, postfix)
```

This fix makes `total` to be `0` when `total` is `None`, ensuring that the operations can be performed while maintaining the original logic where a total of `None` resulted in a progress bar with only basic progress statistics displayed.