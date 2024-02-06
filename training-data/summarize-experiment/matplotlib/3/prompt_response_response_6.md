The bug is caused by the incorrect initialization of the `_filled` attribute in the `_recache` method of the `MarkerStyle` class. The buggy function sets `_filled` to `True` unconditionally, which contradicts the expected behavior when using `fillstyle='none'`.

To fix the bug, the `_filled` attribute should be set based on the value of the `fillstyle` parameter. If the `fillstyle` is set to `'none'`, then `_filled` should be set to `False`, indicating that the marker should be hollow. Otherwise, `_filled` should be set to `True`.

Here's the corrected version of the `_recache` method:

```python
class MarkerStyle():
    # ... omitted code ...

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

With this corrected version, the `_filled` attribute is updated based on the value of `self._fillstyle`. So when `fillstyle` is set to `'none'`, the markers will be hollow.

This fix resolves the issue where markers were not appearing as hollow when using `ax.scatter()` and setting `markers.MarkerStyle()` fillstyle to `'none'`. The corrected implementation ensures that the `_filled` attribute corresponds to the expected behavior when setting the fillstyle.

The GitHub issue title for this bug could be: "Markers are not hollow when using ax.scatter() and setting markers.MarkerStyle()'s fillstyle to 'none'".

The associated detailed issue description could explain the problem and include example code for reproduction, like the one provided.