### Analysis:
The GitHub issue indicates that the markers are not appearing hollow when setting `fillstyle='none'` in a custom `markers.MarkerStyle`. The `scatter` function is used with a custom `MarkerStyle` object to set the markers, but the markers do not display as expected.

### Error Location:
The issue seems to be related to the `_recache` function in the `markers.py` file. The function resets certain properties of the marker, potentially overriding the `fillstyle='none'` set in the custom `MarkerStyle`.

### Cause of the Bug:
The `_recache` function resets the `_filled` property to `True` unconditionally, causing the markers to always be filled regardless of the `fillstyle` set in the `MarkerStyle`. This behavior leads to the markers not appearing hollow as expected.

### Strategy for Fixing the Bug:
To fix the bug, the `_recache` function needs to consider the `fillstyle` set in the `MarkerStyle` and ensure that the `_filled` property reflects the intended filled/hollow state of the marker.

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
    self._filled = self.get_fillstyle() != 'none'
    self._marker_function()
```

By updating the `_filled` property based on the `fillstyle` set in the `MarkerStyle`, the markers will now be displayed as expected, either filled or hollow. This correction addresses the issue reported in the GitHub thread.