The issue with the code is that it tries to multiply `total` with `unit_scale` which results in a TypeError when `total` is None. To fix this issue, I will add a check to set `total` to 0 if it is None.

Here is the fixed code:

```python
@staticmethod
def format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False,
                 unit='it', unit_scale=False, rate=None, bar_format=None,
                 postfix=None, unit_divisor=1000, **extra_kwargs):
    """
    Return a string-based progress bar given some parameters
    Parameters
    ----------
   