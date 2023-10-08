I've made the minimal changes necessary to fix the TypeError and OSError in the `format_meter` function of the given code. I've updated the code to skip the custom scale application when the total is None. Here's the updated function:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    # ... (the code above remains the same)

    # apply custom scale if necessary
    if unit_scale and unit_scale not in (True, 1) and total is not None:
        total *= unit_scale
        n *= unit_scale
        if rate:
            rate *= unit_scale  # by default rate = 1 / self.avg_time
        unit_scale = False

    # ... (the code below remains the same)
```

Now, the test `test_nototal()` should run without any errors, and the bug fix should not affect other successful tests.