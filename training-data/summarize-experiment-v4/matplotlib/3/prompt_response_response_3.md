The potential error location is within the `_recache` function of the `MarkerStyle` class, particularly in how it calls the `_marker_function` method.

The bug is likely caused by the incorrect setting of the `_filled` attribute when the `self._fillstyle` parameter is updated to 'none' in the `_recache` function. This is causing issues with the scatter markers not being hollow when the `fillstyle` is set to 'none'.

To fix the bug, the `_recache` function should be modified to correctly handle the case where the `fillstyle` is set to 'none' to ensure that the markers are hollow when using `ax.scatter`.

Here's the corrected code for the `_recache` function:

```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = None  # Correctly reset self._path to None
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None
    self._snap_threshold = None
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    if self._fillstyle == 'none':
        self._filled = False  # Set _filled to False when fillstyle is 'none'
    else:
        self._filled = True
    self._marker_function()
```

By setting `self._path` to `None` and handling the `_filled` attribute based on the `fillstyle`, the corrected `_recache` function should ensure that scatter markers are hollow when the `fillstyle` is set to 'none', resolving the issue reported on GitHub.