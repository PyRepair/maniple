The bug occurs because the `_filled` attribute is always set to `True` in the `_recache` function, regardless of the `fillstyle` parameter value. This causes the markers to be filled even when the `fillstyle` is set to 'none'.

To fix the bug, we need to check the value of the `fillstyle` parameter and set the `_filled` attribute accordingly. If the `fillstyle` is 'none', `_filled` should be set to `False`, otherwise it should be set to `True`.

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
    self._filled = self._fillstyle != 'none'  # Set _filled based on fillstyle
    self._marker_function()
```

This change ensures that the `_filled` attribute reflects the value of `fillstyle`, allowing the markers to be hollow when the `fillstyle` is set to 'none'.

This fix addresses the issue reported and should resolve the problem of markers not appearing hollow when using `ax.scatter()` and setting `fillstyle` to 'none'.