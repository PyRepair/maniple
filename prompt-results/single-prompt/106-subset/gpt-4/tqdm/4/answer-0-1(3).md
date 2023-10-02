The issue comes from the fact that when computing the progress bar the method tries to multiply `total` with `unit_scale` when `total` is `None`. To fix this, you can add additional safeguard in the `format_meter` function to only do the multiplication when `total` is not `None`.

Here's how you amend the method:

```python
    @staticmethod
    def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                     unit='it', unit_scale=False, rate=None, bar_format=None,
                     postfix=None, unit_divisor=1000, **extra_kwargs):
        # all the proceeding code just as original code
        # apply custom scale if necessary
        if unit_scale and unit_scale not in (True, 1):
            if total is not None:  # only scale total when it's not None
                total *= unit_scale
            n *= unit_scale
            if rate:
                rate *= unit_scale  # by default rate = 1 / self.avg_time
            unit_scale = False
        # all the succeeding code just as original code
``` 

We safely guarded `total *= unit_scale` by surrounding it with an `if` statement checking if `total` is not `None`. The rest of code remains same.