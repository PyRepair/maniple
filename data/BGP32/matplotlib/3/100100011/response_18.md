## Analysis:
1. The `_recache` function in `markers.py` is responsible for recalculating marker properties.
2. The test `test_marker_fillstyle` checks if the marker's fillstyle is correctly set to `'none'`.
3. The issue reported on GitHub indicates that setting `fillstyle='none'` does not produce a hollow marker with `ax.scatter()`.
4. The bug occurs because the `_recache` function sets `self._filled = True`, which overrides the fillstyle 'none' setting.

## Bug Cause:
The bug is caused by setting `_filled` to `True` in the `_recache` function, which forces the marker to be filled regardless of the fillstyle setting. This results in the marker not appearing as hollow when `fillstyle='none'` is used.

## Fix Strategy:
To fix the bug, we need to update the `_recache` function to consider the `fillstyle` setting. If `fillstyle='none'`, then `_filled` should be set to `False` to produce a hollow marker.

## Corrected Version:
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

By updating the `_recache` function to consider the `fillstyle` setting and setting `_filled` accordingly, the corrected version should now produce a hollow marker when `fillstyle='none'` is used.