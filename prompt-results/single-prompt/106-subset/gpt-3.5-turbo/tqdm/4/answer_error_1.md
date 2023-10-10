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
    n  : int
        Number of finished iterations.
    total  : int
        The expected total number of iterations. If meaningless (), only
        basic progress statistics are displayed (no ETA).
    elapsed  : float
        Number of seconds passed since start.
