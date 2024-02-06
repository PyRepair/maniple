The error occurs because the `_filled` attribute is being set to `True` by default in the `_recache` function, instead of being set based on the value of the `fillstyle` attribute.

To fix this issue, we need to update the `_recache` function to set the `_filled` attribute based on the value of the `fillstyle` attribute.

The corrected code for the `_recache` function is as follows:

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
    self._filled = True if self._fillstyle != 'none' else False  # update _filled attribute based on the fillstyle
    self._marker_function()
```

By making this change, the `_recache` function will accurately set the `_filled` attribute based on the `fillstyle` attribute, resolving the issue where markers are not hollow when using `ax.scatter()` and setting the `fillstyle` to 'none'.