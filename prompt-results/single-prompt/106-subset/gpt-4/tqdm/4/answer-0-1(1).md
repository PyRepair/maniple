I found the issue in the `format_meter` function. The multiplication of `total` by `unit_scale` should be skipped if `total` is `None`. I fixed this issue by adding a conditional check before applying the custom scale. Here is the modified `format_meter` function:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    #... (previous part of the code is not changed)
    
    # apply custom scale if necessary
    if unit_scale and unit_scale not in (True, 1):
        if total is not None:
            total *= unit_scale
        n *= unit_scale
        if rate:
            rate *= unit_scale  # by default rate = 1 / self.avg_time
        unit_scale = False

    #... (rest of the code is not changed)
```

With this fix, the test should now pass without errors.