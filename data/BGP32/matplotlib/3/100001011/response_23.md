## Analysis:
The issue is the markers not appearing as hollow when using `ax.scatter()` and setting `markers.MarkerStyle()`'s `fillstyle` to `'none'`. This behavior arises from the `_recache` function not properly handling the `fillstyle` parameter, which leads to markers being filled instead of hollow.

### Error Location:
The `self._filled` variable is set to `True` unconditionally in the `_recache` function, which causes the markers to be filled regardless of the `fillstyle` parameter.

### Bug Cause:
The bug is caused by the `_recache` function setting `self._filled` to `True` even when the `fillstyle` is intended to be `'none'`. This prevents the markers from being hollow as expected.

### Fix Strategy:
To fix the bug, we need to check the `fillstyle` parameter in the `_recache` function and set `self._filled` accordingly. If the `fillstyle` is `'none'`, we should set `self._filled` to `False` to ensure hollow markers.

### Corrected Version:
Here is the corrected version of the `_recache` function:

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
    if self.get_fillstyle() == 'none':  # Check fillstyle parameter
        self._filled = False
    else:
        self._filled = True
    self._marker_function()
```

By checking the `fillstyle` parameter in the `_recache` function and setting the `self._filled` variable accordingly, we ensure that markers will be hollow when `fillstyle` is set to `'none'`. This fix addresses the issue reported on GitHub.