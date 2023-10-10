The issue seems to be with the line `total *= unit_scale` where `total` is None. In order to fix this, we can assign the value `total` to another variable and then multiply it with `unit_scale`. Here is the fixed code snippet:

```python
