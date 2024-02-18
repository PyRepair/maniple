The potential error location within the original code is the condition `if self._marker_function is None`, as it always returns immediately without performing the intended recaching.

The bug's cause is that the `_recache` function wrongly returns if `self._marker_function` is None, preventing the intended recaching from being performed.

To fix the bug, the `if` condition should be modified to check if `_marker_function` is not None, and perform the recaching if it's True.

Here's the corrected code:
```python
def _recache(self):
    if self._marker_function is not None:  # Modified condition to check if _marker_function is not None
        self._path = _empty_path
        self._transform = IdentityTransform()
        self._alt_path = None
        self._alt_transform = None
        self._snap_threshold = None
        self._joinstyle = 'round'
        self._capstyle = 'butt'
        self._filled = True
        self._marker_function()
```

With this correction, the issue related to markers not being hollow when using `ax.scatter()` and setting `markers.MarkerStyle()`'s `fillstyle` to `'none'` should be resolved.