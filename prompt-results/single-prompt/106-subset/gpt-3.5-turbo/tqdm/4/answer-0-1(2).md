To fix the bug in the `format_meter` method, you can simply replace the line `total *= unit_scale` with `total = total * unit_scale if total else None`. This change ensures that the multiplication operation is only performed if `total` is not `None`. If `total` is `None`, it remains `None`.

Here's the fixed code:

```python
@staticmethod
def format_meter