### Potential error locations:
1. The `_filled` attribute is set to `True` in the `_recache` function, which should be `False` when the `fillstyle='none'`.
2. The `is_filled` method in the `MarkerStyle` class might not be returning the correct value based on the `filled` attribute.

### Cause of the bug:
The bug is caused by the `is_filled` method in the `MarkerStyle` class not returning the correct value. The `_filled` attribute is set to `True` in the `_recache` function, but it should be `False` when `fillstyle='none'`. This leads to the test failing with `assert not True`.

### Strategy for fixing the bug:
1. Update the `_recache` function to set `_filled` to `False` when the `fillstyle='none'`.
2. Ensure that the `is_filled` method returns the correct value based on the `_filled` attribute.

### Corrected version of the `_recache` function:
```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = _empty_path
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None
    self._snap_threshold = None
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    self._filled = self._fillstyle != 'none'
    self._marker_function()
```

After applying this correction, the issue with the hollow markers not appearing when setting `fillstyle='none'` should be resolved.