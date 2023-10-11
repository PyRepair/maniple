The issue with the code is that the `total` variable could be `None` and then it tries to multiply `None` with `unit_scale` in the following lines:

```python
# apply custom scale if necessary
if unit_scale and unit_scale not in (True, 1):
    total *= unit_scale
    n *= unit_scale
    if rate:
        rate *= unit_scale  # by default rate = 1 / self.avg_time
    unit_scale = False
```

To fix this issue, we can change the `total *= unit_scale` line to check if `total` is not `None` before multiplying it with