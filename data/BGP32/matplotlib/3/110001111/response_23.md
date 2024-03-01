## Analysis
1. The buggy function `_recache` is inside the `MarkerStyle` class in the file `markers.py`. It resets various attributes of `MarkerStyle` but fails to correctly set the `filled` attribute.
2. The bug is causing markers to not be hollow when using `ax.scatter()` with `fillstyle='none'`.
3. The bug occurs because the `_filled` attribute is always set to `True` regardless of the `fillstyle` parameter passed to `MarkerStyle`, hence resulting in filled markers.
4. To fix the bug, we need to ensure that the `_filled` attribute of `MarkerStyle` is correctly set based on the `fillstyle` parameter passed when creating an instance of `MarkerStyle`.

## Bug Fix
```python
class MarkerStyle():

    def __init__(self, marker='o', fillstyle='full'):
        self._marker_function = self.get_path(marker)
        self._fillstyle = fillstyle
        self._recache()

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
        self._filled = self._fillstyle.lower() != 'none'
        self._marker_function()
```

With this fix, the `MarkerStyle` class constructor now initializes the `_fillstyle` attribute, and the `_filled` attribute is correctly set based on the `fillstyle` parameter passed. This ensures that setting `fillstyle='none'` will result in hollow markers when used with `ax.scatter()`.