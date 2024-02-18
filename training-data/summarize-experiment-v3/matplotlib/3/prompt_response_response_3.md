The issue seems to be related to markers not appearing as hollow even when the `fillstyle` parameter is set to 'none' when using `ax.scatter()` with a custom `markers.MarkerStyle`. This might be due to the `_recache` function unconditionally setting `self._filled` to `True`, which contradicts the expected behavior when `fillstyle` is set to 'none'.

To fix the bug:
1. Update the `_recache` function to correctly handle the `fillstyle` parameter and ensure that the `self._filled` attribute reflects the desired marker fill style.

Here's the corrected code for the `_recache` function:
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
    self._filled = self._fillstyle != 'none'  # Check the fillstyle parameter
    self._marker_function()
```

With this correction, the `_recache` function now correctly checks the `fillstyle` parameter and sets `self._filled` accordingly, ensuring that markers are correctly displayed as hollow when `fillstyle='none'`.

This change should resolve the issue reported on GitHub and ensure that the markers appear as hollow when `fillstyle='none'` is used with `ax.scatter()` and custom `markers.MarkerStyle`.