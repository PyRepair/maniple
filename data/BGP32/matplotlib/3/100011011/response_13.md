### Analysis:
1. The `MarkerStyle` class is not properly handling the case when `fillstyle='none'` is set, as shown in the failing test and the GitHub issue.
2. The `_recache` function is responsible for setting up the marker properties, including whether the marker is filled or not.

### Bug Cause:
The `_filled` attribute is set to `True` by default in the `_recache` function, causing the markers to be filled even when `fillstyle='none'` is specified.

### Fix Strategy:
Update the `_recache` function to correctly handle the `fillstyle='none'` case by setting `_filled` to `False`.

### Corrected Version:
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
    self._filled = True  # Corrected to set _filled to False for 'none' fillstyle
    if self.get_fillstyle() == 'none':
        self._filled = False
    self._marker_function()
``` 

After making this correction, the test for `marker_style.is_filled()` should pass successfully and the markers in `ax.scatter()` should be hollow when `fillstyle='none'` is set.